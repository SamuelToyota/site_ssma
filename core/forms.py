from django import forms
from .models import MentoriaContato


class MentoriaContatoForm(forms.ModelForm):
    class Meta:
        model = MentoriaContato
        fields = ['nome', 'email', 'mensagem']
        widgets = {
            'nome': forms.TextInput(attrs={
                'placeholder': 'Digite seu nome completo',
            }),
            'email': forms.EmailInput(attrs={
                'placeholder': 'Digite seu melhor e-mail',
            }),
            'mensagem': forms.Textarea(attrs={
                'placeholder': 'Conte brevemente seu momento profissional, seus desafios e o que você deseja desenvolver.',
                'rows': 7,
            }),
        }