from urllib.parse import urlparse, parse_qs

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, redirect, render

from .forms import MentoriaContatoForm
from .models import (
    Aula,
    Curso,
    Material,
    Matricula,
    MentoriaAula,
    Modulo,
    ProgressoAula,
)


def home(request):
    return render(request, "home.html")


def formacao(request):
    return render(request, "formacao.html")


def videos(request):
    return render(request, "videos.html")


def contato(request):
    if request.method == "POST":
        form = MentoriaContatoForm(request.POST)
        if form.is_valid():
            contato_obj = form.save()

            assunto = "Nova solicitação de Mentoria Diagnóstica"
            mensagem = (
                f"Nome: {contato_obj.nome}\n"
                f"E-mail: {contato_obj.email}\n\n"
                f"Mensagem:\n{contato_obj.mensagem}"
            )

            send_mail(
                subject=assunto,
                message=mensagem,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[settings.CONTACT_EMAIL],
                fail_silently=False,
            )
            return redirect("sucesso")
    else:
        form = MentoriaContatoForm()

    return render(request, "contato.html", {"form": form})


def sucesso(request):
    return render(request, "sucesso.html")


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
def modulos(request):
    return render(request, "modulos.html")