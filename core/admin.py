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


class ModuloInline(admin.TabularInline):
    model = Modulo
    extra = 0
    fields = ("titulo", "ordem")
    ordering = ("ordem",)


class AulaInline(admin.TabularInline):
    model = Aula
    extra = 0
    fields = ("titulo", "ordem", "video_url")
    ordering = ("ordem",)


@admin.register(MentoriaContato)
class MentoriaContatoAdmin(admin.ModelAdmin):
    list_display = ("nome", "email", "criado_em")
    search_fields = ("nome", "email", "mensagem")
    list_filter = ("criado_em",)
    ordering = ("-criado_em",)


@admin.register(PerfilAluno)
class PerfilAlunoAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "nome_exibicao",
        "telefone",
        "acesso_ativo",
        "origem_compra",
        "compra_id",
    )
    search_fields = (
        "user__username",
        "user__email",
        "nome_exibicao",
        "telefone",
        "compra_id",
    )
    list_filter = ("acesso_ativo", "origem_compra")
    autocomplete_fields = ("user",)


@admin.register(Curso)
class CursoAdmin(admin.ModelAdmin):
    list_display = ("titulo", "slug", "ativo")
    list_filter = ("ativo",)
    search_fields = ("titulo", "descricao")
    prepopulated_fields = {"slug": ("titulo",)}
    inlines = [ModuloInline]


@admin.register(Matricula)
class MatriculaAdmin(admin.ModelAdmin):
    list_display = (
        "aluno",
        "curso",
        "ativa",
        "origem_pagamento",
        "codigo_pagamento",
        "criado_em",
    )
    list_filter = ("ativa", "curso", "origem_pagamento")
    search_fields = (
        "aluno__username",
        "aluno__email",
        "curso__titulo",
        "codigo_pagamento",
    )
    autocomplete_fields = ("aluno", "curso")
    ordering = ("-criado_em",)


@admin.register(Modulo)
class ModuloAdmin(admin.ModelAdmin):
    list_display = ("titulo", "curso", "ordem")
    list_filter = ("curso",)
    search_fields = ("titulo", "descricao", "curso__titulo")
    autocomplete_fields = ("curso",)
    ordering = ("curso", "ordem")
    inlines = [AulaInline]


@admin.register(Aula)
class AulaAdmin(admin.ModelAdmin):
    list_display = ("titulo", "modulo", "curso_nome", "ordem")
    list_filter = ("modulo__curso", "modulo")
    search_fields = ("titulo", "descricao", "modulo__titulo", "modulo__curso__titulo")
    autocomplete_fields = ("modulo",)
    ordering = ("modulo__curso", "modulo__ordem", "ordem")

    @admin.display(description="Curso")
    def curso_nome(self, obj):
        return obj.modulo.curso.titulo


@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
    list_display = ("titulo", "curso", "possui_link")
    list_filter = ("curso",)
    search_fields = ("titulo", "descricao", "curso__titulo")
    autocomplete_fields = ("curso",)

    @admin.display(boolean=True, description="Link")
    def possui_link(self, obj):
        return bool(obj.link)


@admin.register(MentoriaAula)
class MentoriaAulaAdmin(admin.ModelAdmin):
    list_display = ("titulo", "curso", "data_referencia", "possui_gravacao")
    list_filter = ("curso", "data_referencia")
    search_fields = ("titulo", "descricao", "curso__titulo")
    autocomplete_fields = ("curso",)
    ordering = ("-data_referencia",)

    @admin.display(boolean=True, description="Gravação")
    def possui_gravacao(self, obj):
        return bool(obj.link_gravacao)


@admin.register(ProgressoAula)
class ProgressoAulaAdmin(admin.ModelAdmin):
    list_display = ("aluno", "aula", "curso_nome", "concluida", "atualizado_em")
    list_filter = ("concluida", "aula__modulo__curso")
    search_fields = (
        "aluno__username",
        "aluno__email",
        "aula__titulo",
        "aula__modulo__titulo",
        "aula__modulo__curso__titulo",
    )
    autocomplete_fields = ("aluno", "aula")
    ordering = ("-atualizado_em",)

    @admin.display(description="Curso")
    def curso_nome(self, obj):
        return obj.aula.modulo.curso.titulo