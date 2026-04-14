from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import redirect, render

from .forms import MentoriaContatoForm


def home(request):
    return render(request, 'home.html')


def formacao(request):
    return render(request, 'formacao.html')


def videos(request):
    return render(request, 'videos.html')


def contato(request):
    if request.method == 'POST':
        form = MentoriaContatoForm(request.POST)
        if form.is_valid():
            contato_obj = form.save()

            assunto = 'Nova solicitação de Mentoria Diagnóstica'
            mensagem = (
                f'Nome: {contato_obj.nome}\n'
                f'E-mail: {contato_obj.email}\n\n'
                f'Mensagem:\n{contato_obj.mensagem}'
            )

            send_mail(
                subject=assunto,
                message=mensagem,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[settings.CONTACT_EMAIL],
                fail_silently=True,
            )

            return redirect('sucesso')
    else:
        form = MentoriaContatoForm()

    return render(request, 'contato.html', {'form': form})


def sucesso(request):
    return render(request, 'sucesso.html')