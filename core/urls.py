from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("formacao/", views.formacao, name="formacao"),
    path("videos/", views.videos, name="videos"),
    path("modulos/", views.modulos, name="modulos"),
    path("contato/", views.contato, name="contato"),
    path("sucesso/", views.sucesso, name="sucesso"),

    path("aluno/", views.aluno_dashboard, name="aluno_dashboard"),
    path("aluno/modulos/", views.aluno_modulos, name="aluno_modulos"),
    path(
        "aluno/modulos/<int:modulo_id>/",
        views.aluno_modulo_detalhe,
        name="aluno_modulo_detalhe",
    ),
    path("aluno/aula/<int:aula_id>/", views.aluno_aula, name="aluno_aula"),
    path("aluno/materiais/", views.aluno_materiais, name="aluno_materiais"),
    path("aluno/mentorias/", views.aluno_mentorias, name="aluno_mentorias"),
    path("aluno/perfil/", views.aluno_perfil, name="aluno_perfil"),
]