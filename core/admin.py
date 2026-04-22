from django.contrib import admin

from .models import (
    Aula,
    Curso,
    Material,
    Matricula,
    MentoriaAula,
    MentoriaContato,
    Modulo,
    PerfilAluno,
    ProgressoAula,
)


@admin.register(MentoriaContato)
class MentoriaContatoAdmin(admin.ModelAdmin):
    list_display = ("nome", "email", "criado_em")
    search_fields = ("nome", "email")
    list_filter = ("criado_em",)


@admin.register(PerfilAluno)
class PerfilAlunoAdmin(admin.ModelAdmin):
    list_display = ("user", "nome_exibicao", "acesso_ativo", "compra_id")
    search_fields = ("user__username", "nome_exibicao", "compra_id")


@admin.register(Curso)
class CursoAdmin(admin.ModelAdmin):
    list_display = ("titulo", "slug", "ativo")
    prepopulated_fields = {"slug": ("titulo",)}


@admin.register(Matricula)
class MatriculaAdmin(admin.ModelAdmin):
    list_display = ("aluno", "curso", "ativa", "origem_pagamento", "codigo_pagamento")
    list_filter = ("ativa", "curso")
    search_fields = ("aluno__username", "curso__titulo", "codigo_pagamento")


@admin.register(Modulo)
class ModuloAdmin(admin.ModelAdmin):
    list_display = ("titulo", "curso", "ordem")
    list_filter = ("curso",)


@admin.register(Aula)
class AulaAdmin(admin.ModelAdmin):
    list_display = ("titulo", "modulo", "ordem")
    list_filter = ("modulo__curso", "modulo")


@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
    list_display = ("titulo", "curso")


@admin.register(MentoriaAula)
class MentoriaAulaAdmin(admin.ModelAdmin):
    list_display = ("titulo", "curso", "data_referencia")


@admin.register(ProgressoAula)
class ProgressoAulaAdmin(admin.ModelAdmin):
    list_display = ("aluno", "aula", "concluida", "atualizado_em")
    list_filter = ("concluida",)