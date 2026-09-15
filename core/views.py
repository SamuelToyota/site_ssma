import logging
from urllib.parse import parse_qs, urlparse

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from .forms import (
    CadastroAlunoForm,
    ContatoForm,
    EmpresaContatoForm,
    MentoriaContatoForm,
    NewsletterLeadForm,
)
from .models import (
    Artigo,
    Aula,
    Case,
    CategoriaConteudo,
    Depoimento,
    FAQ,
    Material,
    Matricula,
    MentoriaAula,
    Modulo,
    NewsletterLead,
    ProgressoAula,
)

logger = logging.getLogger(__name__)

METHOD_DIMENSIONS = [
    {
        "letter": "D",
        "name": "Diagnóstico Estratégico",
        "description": "Enxergar riscos, causas e oportunidades além da demanda imediata da operação.",
    },
    {
        "letter": "E",
        "name": "Enquadramento",
        "description": "Organizar a leitura do contexto e posicionar a contribuição de SSMA para o negócio.",
    },
    {
        "letter": "S",
        "name": "Sistemas de Impacto",
        "description": "Estruturar rotinas, indicadores e práticas que tornem o avanço visível e sustentável.",
    },
    {
        "letter": "T",
        "name": "Táticas de Influência",
        "description": "Apresentar prioridades, conduzir conversas e construir apoio para decisões relevantes.",
    },
    {
        "letter": "A",
        "name": "Alianças",
        "description": "Conectar áreas e pessoas capazes de transformar uma proposta em ação coordenada.",
    },
    {
        "letter": "Q",
        "name": "Quebra de Crenças",
        "description": "Revisar padrões que limitam a presença, a comunicação e a atuação consultiva.",
    },
    {
        "letter": "U",
        "name": "Ultravalor",
        "description": "Traduzir entregas técnicas em impacto sobre risco, operação, cultura e resultado.",
    },
    {
        "letter": "E",
        "name": "Evolução",
        "description": "Transformar aprendizado em um plano contínuo de desenvolvimento e aplicação.",
    },
]

EDITORIAL_TOPICS = [
    "Cultura de Segurança",
    "Liderança",
    "Gestão de Riscos",
    "SSMA Estratégico",
    "Comunicação",
    "Carreira",
    "ESG",
]


def _render_page(
    request,
    template_name,
    context=None,
    *,
    title,
    description,
    og_type="website",
    status=200,
):
    page_context = {
        "page_title": title,
        "page_description": description,
        "og_type": og_type,
    }
    if context:
        page_context.update(context)
    return render(request, template_name, page_context, status=status)


def _notify_contact(contact):
    subject_labels = dict(contact.INTERESSE_CHOICES)
    lines = [
        f"Interesse: {subject_labels.get(contact.tipo_interesse, contact.tipo_interesse)}",
        f"Nome: {contact.nome}",
        f"E-mail: {contact.email}",
    ]
    if contact.telefone:
        lines.append(f"Telefone: {contact.telefone}")
    if contact.empresa:
        lines.append(f"Empresa: {contact.empresa}")
    if contact.cargo:
        lines.append(f"Cargo: {contact.cargo}")
    lines.extend(["", "Mensagem:", contact.mensagem])

    try:
        send_mail(
            subject=f"Novo contato | {subject_labels.get(contact.tipo_interesse, 'Site')}",
            message="\n".join(lines),
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[settings.CONTACT_EMAIL],
            fail_silently=False,
        )
    except Exception:
        logger.exception("Falha ao enviar notificação do contato id=%s", contact.pk)


def _contact_page(
    request,
    *,
    form_class,
    template_name,
    title,
    description,
    origin,
    extra_context=None,
):
    form = form_class(request.POST or None)
    if request.method == "POST" and form.is_valid():
        contact = form.save(commit=False)
        contact.origem = origin
        contact.save()
        _notify_contact(contact)
        return redirect(f"{reverse('sucesso')}?origem={origin}")

    context = {"form": form}
    if extra_context:
        context.update(extra_context)
    return _render_page(
        request,
        template_name,
        context,
        title=title,
        description=description,
    )


def home(request):
    newsletter_form = NewsletterLeadForm(request.POST or None)
    if request.method == "POST" and request.POST.get("form_type") == "newsletter":
        if newsletter_form.is_valid():
            NewsletterLead.objects.update_or_create(
                email=newsletter_form.cleaned_data["email"].strip().lower(),
                defaults={
                    "nome": newsletter_form.cleaned_data["nome"].strip(),
                    "origem": "home",
                    "ativo": True,
                },
            )
            messages.success(
                request,
                "Inscrição recebida. Você passará a receber os próximos conteúdos.",
            )
            return redirect(f"{reverse('home')}?newsletter=ok#newsletter")
    elif request.method == "POST":
        newsletter_form = NewsletterLeadForm()

    context = {
        "method_dimensions": METHOD_DIMENSIONS,
        "editorial_topics": EDITORIAL_TOPICS,
        "latest_articles": Artigo.objects.publicados().select_related("categoria")[:3],
        "testimonials": Depoimento.objects.filter(ativo=True)[:3],
        "newsletter_form": newsletter_form,
    }
    return _render_page(
        request,
        "home.html",
        context,
        title="Formação e Mentoria em SSMA | Consultor Interno",
        description=(
            "Formação, mentoria e desenvolvimento para profissionais de Segurança do Trabalho "
            "e SSMA que querem participar das decisões do negócio."
        ),
    )

def curso_cultura(request):
    return _render_page(
        request,
        "core/curso_cultura.html",
        {"faqs": FAQ.objects.filter(pagina="curso_cultura", ativa=True)},
        title="Especialista em Cultura de Segurança | Consultor Interno",
        description=(
            "Formação para profissionais de SSMA que querem diagnosticar, mobilizar lideranças "
            "e sustentar uma cultura de segurança além do compliance."
        ),
    )

def curso_teste(request):
    return _render_page(
        request,
        "core/curso_teste.html",
        {"faqs": FAQ.objects.filter(pagina="curso_teste", ativa=True)},
        title="Perfil, Valores Pessoais e Carreira | Consultor Interno",
        description=(
            "Diagnóstico individual para compreender valores, organizar critérios e tomar "
            "decisões profissionais com mais clareza."
        ),
    )

def cursos(request):
    return _render_page(
        request,
        "core/cursos.html",
        {"faqs": FAQ.objects.filter(pagina="cursos", ativa=True)},
        title="Formações em SSMA e Desenvolvimento Profissional | Consultor Interno",
        description=(
            "Conheça as formações e diagnósticos do Consultor Interno para cultura de segurança, "
            "influência e desenvolvimento profissional."
        ),
    )


def formacoes(request):
    return redirect("cursos", permanent=True)


def mentoria(request):
    return _contact_page(
        request,
        form_class=MentoriaContatoForm,
        template_name="mentoria.html",
        title="Mentoria para Profissionais de SSMA | Consultor Interno",
        description=(
            "Mentoria individual para profissionais de SSMA que precisam organizar prioridades, "
            "comunicar valor e ampliar sua participação nas decisões."
        ),
        origin="mentoria",
        extra_context={
            "faqs": FAQ.objects.filter(pagina="mentoria", ativa=True),
        },
    )


def para_empresas(request):
    context_response = _contact_page(
        request,
        form_class=EmpresaContatoForm,
        template_name="para_empresas.html",
        title="Treinamentos e Desenvolvimento em SSMA para Empresas | Consultor Interno",
        description=(
            "Desenvolvimento de lideranças e profissionais para conectar segurança, cultura, "
            "comportamento e decisões organizacionais."
        ),
        origin="empresas",
        extra_context={
            "faqs": FAQ.objects.filter(pagina="empresas", ativa=True),
            "cases": Case.objects.filter(publicado=True),
        },
    )
    return context_response


def sobre(request):
    return _render_page(
        request,
        "sobre.html",
        {"method_dimensions": METHOD_DIMENSIONS},
        title="Alan Silvério e o Consultor Interno | Sobre",
        description=(
            "Conheça Alan Silvério, engenheiro de segurança com mais de 20 anos de atuação em "
            "SSMA, ESG e Cultura de Segurança."
        ),
    )


def conteudos(request):
    articles = Artigo.objects.publicados().select_related("categoria")
    selected_category = None
    category_slug = request.GET.get("categoria", "").strip()
    if category_slug:
        selected_category = CategoriaConteudo.objects.filter(
            slug=category_slug,
            ativa=True,
        ).first()
        if selected_category:
            articles = articles.filter(categoria=selected_category)

    return _render_page(
        request,
        "conteudos/lista.html",
        {
            "articles": articles,
            "categories": CategoriaConteudo.objects.filter(ativa=True),
            "selected_category": selected_category,
            "editorial_topics": EDITORIAL_TOPICS,
        },
        title="Conteúdos sobre SSMA, Liderança e Cultura de Segurança",
        description=(
            "Artigos de Alan Silvério sobre SSMA estratégico, cultura de segurança, liderança, "
            "gestão de riscos, comunicação e carreira."
        ),
    )


def artigo_detalhe(request, slug):
    article = get_object_or_404(
        Artigo.objects.publicados().select_related("categoria"),
        slug=slug,
    )
    related = (
        Artigo.objects.publicados()
        .filter(categoria=article.categoria)
        .exclude(pk=article.pk)[:3]
    )
    return _render_page(
        request,
        "conteudos/detalhe.html",
        {"article": article, "related_articles": related},
        title=article.meta_titulo or f"{article.titulo} | Consultor Interno",
        description=article.meta_descricao or article.resumo,
        og_type="article",
    )


def politica_privacidade(request):
    return _render_page(
        request,
        "legal/privacidade.html",
        title="Política de Privacidade | Consultor Interno",
        description="Saiba como o Consultor Interno coleta, utiliza e protege os dados enviados pelo site.",
    )


def termos(request):
    return _render_page(
        request,
        "legal/termos.html",
        title="Termos de Uso | Consultor Interno",
        description="Consulte as condições de uso do site Consultor Interno.",
    )


def robots_txt(request):
    content = "\n".join(
        [
            "User-agent: *",
            "Allow: /",
            "Disallow: /admin/",
            "Disallow: /aluno/",
            f"Sitemap: {settings.SITE_URL}/sitemap.xml",
        ]
    )
    return HttpResponse(content, content_type="text/plain; charset=utf-8")


def erro_404(request, exception):
    return _render_page(
        request,
        "404.html",
        status=404,
        title="Página não encontrada | Consultor Interno",
        description="A página solicitada não foi encontrada.",
    )

def formacao(request):
    return redirect("curso_cultura", permanent=True)


def videos(request):
    return redirect("curso_cultura", permanent=True)


def modulos(request):
    return redirect("curso_cultura", permanent=True)


def contato(request):
    initial_interest = request.GET.get("interesse", "")
    allowed_interests = {choice[0] for choice in MentoriaContatoForm.Meta.model.INTERESSE_CHOICES}
    form = ContatoForm(
        request.POST or None,
        initial={
            "tipo_interesse": initial_interest if initial_interest in allowed_interests else "mentoria"
        },
    )
    if request.method == "POST" and form.is_valid():
        contact = form.save(commit=False)
        contact.origem = "contato"
        contact.save()
        _notify_contact(contact)
        return redirect(f"{reverse('sucesso')}?origem=contato")

    return _render_page(
        request,
        "contato.html",
        {"form": form},
        title="Contato | Consultor Interno",
        description=(
            "Fale sobre formações, mentoria, palestras, treinamentos corporativos ou outros "
            "projetos relacionados a SSMA."
        ),
    )


def sucesso(request):
    origin = request.GET.get("origem", "contato")
    return _render_page(
        request,
        "sucesso.html",
        {"origin": origin},
        title="Solicitação recebida | Consultor Interno",
        description="Sua solicitação foi recebida pelo Consultor Interno.",
    )


def cadastro(request):
    if request.method == "POST":
        form = CadastroAlunoForm(request.POST)
        if form.is_valid():
            user = form.save()

            assunto = "Conta criada com sucesso | Área do Aluno"
            mensagem = (
                f"Olá, {user.first_name}!\n\n"
                "Sua conta foi criada com sucesso na Área do Aluno do Consultor Interno.\n\n"
                "Agora você já pode acessar a plataforma utilizando seu login e sua senha.\n\n"
                "Importante:\n"
                "- O conteúdo completo será liberado somente após a matrícula ativa.\n"
                "- Você pode voltar e entrar novamente quando quiser pela página de login.\n\n"
                "Atenciosamente,\n"
                "Equipe Consultor Interno"
            )

            send_mail(
                subject=assunto,
                message=mensagem,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user.email],
                fail_silently=True,
            )

            login(request, user)
            return redirect("aluno_dashboard")
    else:
        form = CadastroAlunoForm()

    return render(request, "aluno/cadastro.html", {"form": form})


def _usuario_tem_acesso(user, curso):
    return Matricula.objects.filter(
        aluno=user,
        curso=curso,
        ativa=True,
    ).exists()


def _youtube_embed_url(url):
    if not url:
        return ""

    if "youtube.com/embed/" in url:
        return url

    parsed = urlparse(url)

    if "youtu.be" in parsed.netloc:
        video_id = parsed.path.strip("/")
        return f"https://www.youtube.com/embed/{video_id}"

    if "youtube.com" in parsed.netloc:
        query = parse_qs(parsed.query)
        video_id = query.get("v", [""])[0]
        if video_id:
            return f"https://www.youtube.com/embed/{video_id}"

    return url


@login_required
def aluno_dashboard(request):
    matricula = (
        Matricula.objects.select_related("curso")
        .filter(aluno=request.user, ativa=True)
        .first()
    )

    curso = matricula.curso if matricula else None
    modulos = curso.modulos.all() if curso else []
    aulas = Aula.objects.filter(modulo__curso=curso) if curso else Aula.objects.none()
    materiais = curso.materiais.all() if curso else Material.objects.none()

    total_aulas = aulas.count()
    concluidas = ProgressoAula.objects.filter(
        aluno=request.user,
        aula__modulo__curso=curso,
        concluida=True,
    ).count()

    progresso_percentual = 0
    if total_aulas > 0:
        progresso_percentual = int((concluidas / total_aulas) * 100)

    proxima_aula = (
        aulas.exclude(
            id__in=ProgressoAula.objects.filter(
                aluno=request.user,
                concluida=True,
            ).values_list("aula_id", flat=True)
        ).first()
        if curso
        else None
    )

    context = {
        "curso": curso,
        "modulos": modulos,
        "materiais_count": materiais.count() if curso else 0,
        "total_aulas": total_aulas,
        "concluidas": concluidas,
        "progresso_percentual": progresso_percentual,
        "proxima_aula": proxima_aula,
        "tem_matricula": bool(curso),
    }
    return render(request, "aluno/dashboard.html", context)


@login_required
def aluno_modulos(request):
    matricula = (
        Matricula.objects.select_related("curso")
        .filter(aluno=request.user, ativa=True)
        .first()
    )
    curso = matricula.curso if matricula else None
    modulos = curso.modulos.prefetch_related("aulas").all() if curso else []

    return render(
        request,
        "aluno/modulos.html",
        {
            "curso": curso,
            "modulos": modulos,
            "tem_matricula": bool(curso),
        },
    )


@login_required
def aluno_modulo_detalhe(request, modulo_id):
    modulo = get_object_or_404(Modulo.objects.select_related("curso"), id=modulo_id)

    if not _usuario_tem_acesso(request.user, modulo.curso):
        return redirect("aluno_dashboard")

    aulas = modulo.aulas.all()
    aulas_concluidas_ids = set(
        ProgressoAula.objects.filter(
            aluno=request.user,
            aula__modulo=modulo,
            concluida=True,
        ).values_list("aula_id", flat=True)
    )

    return render(
        request,
        "aluno/modulo_detalhe.html",
        {
            "modulo": modulo,
            "aulas": aulas,
            "aulas_concluidas_ids": aulas_concluidas_ids,
        },
    )


@login_required
def aluno_aula(request, aula_id):
    aula = get_object_or_404(
        Aula.objects.select_related("modulo", "modulo__curso"),
        id=aula_id,
    )

    if not _usuario_tem_acesso(request.user, aula.modulo.curso):
        return redirect("aluno_dashboard")

    progresso, _ = ProgressoAula.objects.get_or_create(
        aluno=request.user,
        aula=aula,
    )

    if request.method == "POST":
        progresso.concluida = True
        progresso.save()
        return redirect("aluno_aula", aula_id=aula.id)

    embed_url = _youtube_embed_url(aula.video_url)

    return render(
        request,
        "aluno/aula.html",
        {
            "aula": aula,
            "embed_url": embed_url,
            "progresso": progresso,
        },
    )


@login_required
def aluno_materiais(request):
    matricula = (
        Matricula.objects.select_related("curso")
        .filter(aluno=request.user, ativa=True)
        .first()
    )
    curso = matricula.curso if matricula else None
    materiais = curso.materiais.all() if curso else Material.objects.none()

    return render(
        request,
        "aluno/materiais.html",
        {
            "curso": curso,
            "materiais": materiais,
            "tem_matricula": bool(curso),
        },
    )


@login_required
def aluno_mentorias(request):
    matricula = (
        Matricula.objects.select_related("curso")
        .filter(aluno=request.user, ativa=True)
        .first()
    )
    curso = matricula.curso if matricula else None
    mentorias = curso.mentorias.all() if curso else MentoriaAula.objects.none()

    return render(
        request,
        "aluno/mentorias.html",
        {
            "curso": curso,
            "mentorias": mentorias,
            "tem_matricula": bool(curso),
        },
    )


@login_required
def aluno_perfil(request):
    perfil = getattr(request.user, "perfil_aluno", None)

    return render(
        request,
        "aluno/perfil.html",
        {
            "perfil": perfil,
        },
    )
