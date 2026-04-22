from django.conf import settings
from django.db import models


class MentoriaContato(models.Model):
    nome = models.CharField(max_length=150)
    email = models.EmailField()
    mensagem = models.TextField()
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Solicitação de Mentoria"
        verbose_name_plural = "Solicitações de Mentoria"
        ordering = ["-criado_em"]

    def __str__(self) -> str:
        return f"{self.nome} - {self.email}"


class PerfilAluno(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="perfil_aluno",
    )
    nome_exibicao = models.CharField(max_length=150, blank=True)
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