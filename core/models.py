from django.db import models


class MentoriaContato(models.Model):
    nome = models.CharField(max_length=150)
    email = models.EmailField()
    mensagem = models.TextField()
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Solicitação de Mentoria'
        verbose_name_plural = 'Solicitações de Mentoria'
        ordering = ['-criado_em']

    def __str__(self) -> str:
        return f'{self.nome} - {self.email}'