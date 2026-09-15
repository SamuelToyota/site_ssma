from datetime import timedelta

from django.contrib.auth.models import User
from django.core import mail
from django.test import TestCase, override_settings
from django.urls import reverse
from django.utils import timezone

from .models import (
    Artigo,
    Aula,
    CategoriaConteudo,
    Curso,
    Material,
    Matricula,
    MentoriaAula,
    MentoriaContato,
    Modulo,
    NewsletterLead,
    ProgressoAula,
)


@override_settings(
    ALLOWED_HOSTS=["testserver"],
    EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend",
    SITE_URL="https://consultorinterno.com.br",
)
class PublicPagesTests(TestCase):
    def test_public_pages_render(self):
        route_names = [
            "home",
            "cursos",
            "curso_cultura",
            "curso_teste",
            "mentoria",
            "para_empresas",
            "sobre",
            "conteudos",
            "contato",
            "privacidade",
            "termos",
            "login",
            "cadastro",
            "robots_txt",
            "sitemap",
        ]
        for route_name in route_names:
            with self.subTest(route=route_name):
                response = self.client.get(reverse(route_name))
                self.assertEqual(response.status_code, 200)

    def test_old_routes_use_permanent_redirects(self):
        expected = {
            "formacoes": reverse("cursos"),
            "formacao": reverse("curso_cultura"),
            "videos": reverse("curso_cultura"),
            "modulos": reverse("curso_cultura"),
        }
        for route_name, destination in expected.items():
            with self.subTest(route=route_name):
                response = self.client.get(reverse(route_name))
                self.assertRedirects(
                    response,
                    destination,
                    status_code=301,
                    fetch_redirect_response=False,
                )

    def test_home_has_essential_search_metadata(self):
        response = self.client.get(reverse("home"))
        self.assertContains(
            response,
            '<link rel="canonical" href="https://consultorinterno.com.br/">',
            html=True,
        )
        self.assertContains(response, 'property="og:title"')
        self.assertContains(response, 'type="application/ld+json"')

    @override_settings(DEBUG=False)
    def test_custom_404_page(self):
        response = self.client.get("/pagina-inexistente/")
        self.assertEqual(response.status_code, 404)
        self.assertContains(response, "Página não encontrada", status_code=404)

    def test_private_pages_are_noindex(self):
        response = self.client.get(reverse("login"))
        self.assertContains(response, 'content="noindex,nofollow"')

    def test_student_area_redirects_anonymous_users(self):
        response = self.client.get(reverse("aluno_dashboard"))
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse("login"), response.url)

    def test_existing_user_can_login_with_email(self):
        User.objects.create_user(
            username="usuario-legado",
            email="aluno@example.com",
            password="UmaSenhaForte-2026",
        )
        response = self.client.post(
            reverse("login"),
            {"username": "ALUNO@example.com", "password": "UmaSenhaForte-2026"},
        )
        self.assertRedirects(
            response,
            reverse("aluno_dashboard"),
            fetch_redirect_response=False,
        )

    def test_profile_logout_uses_secure_post(self):
        user = User.objects.create_user(
            username="aluno",
            email="outro@example.com",
            password="UmaSenhaForte-2026",
        )
        self.client.force_login(user)
        profile = self.client.get(reverse("aluno_perfil"))
        self.assertContains(profile, f'action="{reverse("logout")}"')
        self.assertNotContains(profile, f'href="{reverse("logout")}"')

        response = self.client.post(reverse("logout"))
        self.assertRedirects(response, reverse("login"), fetch_redirect_response=False)

    def test_authenticated_student_area_renders_without_broken_empty_links(self):
        user = User.objects.create_user(
            username="estudante",
            email="estudante@example.com",
            password="UmaSenhaForte-2026",
        )
        course = Curso.objects.create(
            titulo="Formação de teste",
            slug="formacao-de-teste",
            descricao="Conteúdo criado somente no banco temporário de testes.",
        )
        enrollment = Matricula.objects.create(aluno=user, curso=course, ativa=True)
        module = Modulo.objects.create(curso=course, titulo="Fundamentos", ordem=1)
        lesson = Aula.objects.create(modulo=module, titulo="Aula inicial", ordem=1)
        Material.objects.create(curso=course, titulo="Guia em preparação", link="")
        MentoriaAula.objects.create(
            curso=course,
            titulo="Encontro em preparação",
            link_gravacao="",
        )
        self.assertTrue(enrollment.ativa)
        self.client.force_login(user)

        routes = [
            reverse("aluno_dashboard"),
            reverse("aluno_modulos"),
            reverse("aluno_modulo_detalhe", args=[module.id]),
            reverse("aluno_aula", args=[lesson.id]),
            reverse("aluno_materiais"),
            reverse("aluno_mentorias"),
            reverse("aluno_perfil"),
        ]
        for route in routes:
            with self.subTest(route=route):
                self.assertEqual(self.client.get(route).status_code, 200)

        materials = self.client.get(reverse("aluno_materiais"))
        mentorships = self.client.get(reverse("aluno_mentorias"))
        self.assertContains(materials, "disponível em breve")
        self.assertNotContains(materials, 'href=""')
        self.assertContains(mentorships, "gravação em breve")
        self.assertNotContains(mentorships, 'href="#"')

        response = self.client.post(reverse("aluno_aula", args=[lesson.id]))
        self.assertRedirects(
            response,
            reverse("aluno_aula", args=[lesson.id]),
            fetch_redirect_response=False,
        )
        self.assertTrue(
            ProgressoAula.objects.get(aluno=user, aula=lesson).concluida
        )


@override_settings(
    ALLOWED_HOSTS=["testserver"],
    EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend",
    SITE_URL="https://consultorinterno.com.br",
)
class LeadCaptureTests(TestCase):
    def test_newsletter_creates_and_reactivates_a_lead(self):
        payload = {
            "form_type": "newsletter",
            "nome": "Maria Silva",
            "email": "MARIA@example.com",
            "consentimento": "on",
            "website": "",
        }
        response = self.client.post(reverse("home"), payload)
        self.assertRedirects(
            response,
            f"{reverse('home')}?newsletter=ok#newsletter",
            fetch_redirect_response=False,
        )
        lead = NewsletterLead.objects.get(email="maria@example.com")
        self.assertTrue(lead.ativo)

        lead.ativo = False
        lead.save(update_fields=["ativo"])
        self.client.post(reverse("home"), {**payload, "nome": "Maria S."})
        lead.refresh_from_db()
        self.assertTrue(lead.ativo)
        self.assertEqual(lead.nome, "Maria S.")

    def test_honeypot_blocks_newsletter_spam(self):
        response = self.client.post(
            reverse("home"),
            {
                "form_type": "newsletter",
                "nome": "Robô",
                "email": "robo@example.com",
                "consentimento": "on",
                "website": "https://spam.example",
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertFalse(NewsletterLead.objects.exists())

    def test_general_contact_is_saved_and_notified(self):
        response = self.client.post(
            reverse("contato"),
            {
                "nome": "João Souza",
                "email": "joao@example.com",
                "telefone": "11999999999",
                "tipo_interesse": "mentoria",
                "empresa": "",
                "cargo": "",
                "mensagem": "Quero organizar meu posicionamento profissional.",
                "consentimento": "on",
                "website": "",
            },
        )
        self.assertRedirects(
            response,
            f"{reverse('sucesso')}?origem=contato",
            fetch_redirect_response=False,
        )
        contact = MentoriaContato.objects.get(email="joao@example.com")
        self.assertEqual(contact.tipo_interesse, "mentoria")
        self.assertTrue(contact.consentimento_privacidade)
        self.assertEqual(len(mail.outbox), 1)

    def test_company_form_requires_company_and_role(self):
        response = self.client.post(
            reverse("para_empresas"),
            {
                "nome": "Ana",
                "email": "ana@empresa.com",
                "telefone": "",
                "empresa": "",
                "cargo": "",
                "mensagem": "Precisamos desenvolver nossas lideranças.",
                "consentimento": "on",
                "website": "",
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response.context["form"], "empresa", "Este campo é obrigatório.")
        self.assertFormError(response.context["form"], "cargo", "Este campo é obrigatório.")
        self.assertFalse(MentoriaContato.objects.exists())


@override_settings(
    ALLOWED_HOSTS=["testserver"],
    SITE_URL="https://consultorinterno.com.br",
)
class ContentTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.category = CategoriaConteudo.objects.create(
            nome="Cultura de Segurança",
            slug="cultura-de-seguranca",
        )
        cls.published_article = Artigo.objects.create(
            titulo="Como levar segurança para as decisões",
            slug="seguranca-nas-decisoes",
            resumo="Uma leitura prática sobre influência e prioridades.",
            conteudo="Primeiro parágrafo.\n\nSegundo parágrafo.",
            categoria=cls.category,
            publicado=True,
            publicado_em=timezone.now() - timedelta(days=1),
        )
        cls.draft_article = Artigo.objects.create(
            titulo="Rascunho",
            slug="rascunho",
            resumo="Ainda não publicado.",
            conteudo="Conteúdo em elaboração.",
            categoria=cls.category,
            publicado=False,
        )

    def test_published_article_is_listed_and_rendered(self):
        listing = self.client.get(reverse("conteudos"))
        self.assertContains(listing, self.published_article.titulo)
        self.assertNotContains(listing, self.draft_article.titulo)

        detail = self.client.get(self.published_article.get_absolute_url())
        self.assertEqual(detail.status_code, 200)
        self.assertContains(detail, '"@type": "Article"')

    def test_draft_article_returns_404(self):
        response = self.client.get(self.draft_article.get_absolute_url())
        self.assertEqual(response.status_code, 404)

    def test_sitemap_contains_only_published_articles(self):
        response = self.client.get(reverse("sitemap"))
        body = response.content.decode()
        self.assertIn(self.published_article.get_absolute_url(), body)
        self.assertNotIn(self.draft_article.get_absolute_url(), body)
