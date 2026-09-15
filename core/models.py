from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils import timezone


class MentoriaContato(models.Model):
    INTERESSE_CHOICES = [
        ("formacao", "Quero conhecer uma formação"),
        ("mentoria", "Quero conhecer a mentoria"),
        ("treinamento_empresa", "Quero treinamento para empresa"),
        ("palestra", "Quero conversar sobre uma palestra"),
        ("outro", "Outro assunto"),
    ]

    nome = models.CharField(max_length=150)
    email = models.EmailField()
    telefone = models.CharField(max_length=30, blank=True)
    tipo_interesse = models.CharField(
        max_length=40,
        choices=INTERESSE_CHOICES,
        default="mentoria",
    )
    empresa = models.CharField(max_length=180, blank=True)
    cargo = models.CharField(max_length=120, blank=True)
    mensagem = models.TextField()
    consentimento_privacidade = models.BooleanField(default=False)
    origem = models.CharField(max_length=80, default="site")
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Solicitação de Mentoria"
        verbose_name_plural = "Solicitações de Mentoria"
        ordering = ["-criado_em"]

    def __str__(self) -> str:
        return f"{self.nome} - {self.email}"


class NewsletterLead(models.Model):
    nome = models.CharField(max_length=150)
    email = models.EmailField(unique=True)
    origem = models.CharField(max_length=80, default="site")
    ativo = models.BooleanField(default=True)
    consentimento_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Inscrição na newsletter"
        verbose_name_plural = "Inscrições na newsletter"
        ordering = ["-consentimento_em"]

    def __str__(self) -> str:
        return f"{self.nome} - {self.email}"


class CategoriaConteudo(models.Model):
    nome = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True)
    descricao = models.CharField(max_length=240, blank=True)
    ativa = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Categoria de conteúdo"
        verbose_name_plural = "Categorias de conteúdo"
        ordering = ["nome"]

    def __str__(self) -> str:
        return self.nome


class ArtigoQuerySet(models.QuerySet):
    def publicados(self):
        return self.filter(
            publicado=True,
            publicado_em__lte=timezone.now(),
            categoria__ativa=True,
        )


class Artigo(models.Model):
    titulo = models.CharField(max_length=180)
    slug = models.SlugField(unique=True)
    resumo = models.CharField(max_length=320)
    conteudo = models.TextField()
    categoria = models.ForeignKey(
        CategoriaConteudo,
        on_delete=models.PROTECT,
        related_name="artigos",
    )
    autor = models.CharField(max_length=120, default="Alan Silvério")
    tempo_leitura = models.PositiveSmallIntegerField(default=5)
    imagem_url = models.URLField(blank=True)
    imagem_alt = models.CharField(max_length=180, blank=True)
    meta_titulo = models.CharField(max_length=180, blank=True)
    meta_descricao = models.CharField(max_length=320, blank=True)
    publicado = models.BooleanField(default=False)
    publicado_em = models.DateTimeField(default=timezone.now)
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    objects = ArtigoQuerySet.as_manager()

    class Meta:
        ordering = ["-publicado_em"]

    def __str__(self) -> str:
        return self.titulo

    def get_absolute_url(self):
        return reverse("artigo_detalhe", kwargs={"slug": self.slug})


class Depoimento(models.Model):
    nome = models.CharField(max_length=120)
    cargo = models.CharField(max_length=120, blank=True)
    empresa = models.CharField(max_length=160, blank=True)
    texto = models.TextField()
    ativo = models.BooleanField(default=False)
    ordem = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ["ordem", "nome"]

    def __str__(self) -> str:
        return self.nome


class Case(models.Model):
    titulo = models.CharField(max_length=180)
    slug = models.SlugField(unique=True)
    setor = models.CharField(max_length=120, blank=True)
    situacao = models.TextField()
    problema = models.TextField()
    diagnostico = models.TextField()
    abordagem = models.TextField()
    resultado = models.TextField()
    aprendizado = models.TextField(blank=True)
    publicado = models.BooleanField(default=False)
    ordem = models.PositiveSmallIntegerField(default=0)
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Case"
        verbose_name_plural = "Cases"
        ordering = ["ordem", "-criado_em"]

    def __str__(self) -> str:
        return self.titulo


class FAQ(models.Model):
    PAGINA_CHOICES = [
        ("home", "Página inicial"),
        ("cursos", "Formações"),
        ("curso_cultura", "Cultura de Segurança"),
        ("curso_teste", "Perfil e Carreira"),
        ("mentoria", "Mentoria"),
        ("empresas", "Para empresas"),
    ]

    pagina = models.CharField(max_length=30, choices=PAGINA_CHOICES)
    pergunta = models.CharField(max_length=220)
    resposta = models.TextField()
    ativa = models.BooleanField(default=True)
    ordem = models.PositiveSmallIntegerField(default=0)

    class Meta:
        verbose_name = "Pergunta frequente"
        verbose_name_plural = "Perguntas frequentes"
        ordering = ["pagina", "ordem", "id"]

    def __str__(self) -> str:
        return self.pergunta


class MaterialGratuito(models.Model):
    titulo = models.CharField(max_length=180)
    slug = models.SlugField(unique=True)
    descricao = models.CharField(max_length=320)
    arquivo_url = models.URLField(blank=True)
    ativo = models.BooleanField(default=False)
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Material gratuito"
        verbose_name_plural = "Materiais gratuitos"
        ordering = ["-criado_em"]

    def __str__(self) -> str:
        return self.titulo


class PerfilAluno(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="perfil_aluno",
    )
    nome_exibicao = models.CharField(max_length=150, blank=True)
    telefone = models.CharField(max_length=30, blank=True)
    compra_id = models.CharField(max_length=120, blank=True)
    origem_compra = models.CharField(max_length=80, blank=True)
    acesso_ativo = models.BooleanField(default=False)
    data_liberacao = models.DateTimeField(null=True, blank=True)

    def __str__(self) -> str:
        return self.nome_exibicao or self.user.username


class Curso(models.Model):
    titulo = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    descricao = models.TextField()
    ativo = models.BooleanField(default=True)

    def __str__(self) -> str:
        return self.titulo


class Matricula(models.Model):
    aluno = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="matriculas",
    )
    curso = models.ForeignKey(
        Curso,
        on_delete=models.CASCADE,
        related_name="matriculas",
    )
    ativa = models.BooleanField(default=False)
    origem_pagamento = models.CharField(max_length=100, blank=True)
    codigo_pagamento = models.CharField(max_length=150, blank=True)
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("aluno", "curso")

    def __str__(self) -> str:
        return f"{self.aluno.username} - {self.curso.titulo}"


class Modulo(models.Model):
    curso = models.ForeignKey(
        Curso,
        on_delete=models.CASCADE,
        related_name="modulos",
    )
    titulo = models.CharField(max_length=200)
    descricao = models.TextField(blank=True)
    ordem = models.PositiveIntegerField(default=1)

    class Meta:
        ordering = ["ordem"]

    def __str__(self) -> str:
        return f"{self.curso.titulo} - {self.titulo}"


class Aula(models.Model):
    modulo = models.ForeignKey(
        Modulo,
        on_delete=models.CASCADE,
        related_name="aulas",
    )
    titulo = models.CharField(max_length=200)
    descricao = models.TextField(blank=True)
    video_url = models.URLField(blank=True)
    ordem = models.PositiveIntegerField(default=1)

    class Meta:
        ordering = ["ordem"]

    def __str__(self) -> str:
        return f"{self.modulo.titulo} - {self.titulo}"


class Material(models.Model):
    curso = models.ForeignKey(
        Curso,
        on_delete=models.CASCADE,
        related_name="materiais",
    )
    titulo = models.CharField(max_length=200)
    descricao = models.TextField(blank=True)
    link = models.URLField(blank=True)

    def __str__(self) -> str:
        return self.titulo


class MentoriaAula(models.Model):
    curso = models.ForeignKey(
        Curso,
        on_delete=models.CASCADE,
        related_name="mentorias",
    )
    titulo = models.CharField(max_length=200)
    descricao = models.TextField(blank=True)
    link_gravacao = models.URLField(blank=True)
    data_referencia = models.DateField(null=True, blank=True)

    def __str__(self) -> str:
        return self.titulo


class ProgressoAula(models.Model):
    aluno = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="progressos",
    )
    aula = models.ForeignKey(
        Aula,
        on_delete=models.CASCADE,
        related_name="progressos",
    )
    concluida = models.BooleanField(default=False)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("aluno", "aula")

    def __str__(self) -> str:
        return f"{self.aluno.username} - {self.aula.titulo}"
