from django import forms
from django.contrib.auth.models import User

from .models import MentoriaContato, PerfilAluno


class MentoriaContatoForm(forms.ModelForm):
    class Meta:
        model = MentoriaContato
        fields = ["nome", "email", "mensagem"]
        widgets = {
            "nome": forms.TextInput(
                attrs={"placeholder": "Digite seu nome completo"}
            ),
            "email": forms.EmailInput(
                attrs={"placeholder": "Digite seu melhor e-mail"}
            ),
            "mensagem": forms.Textarea(
                attrs={
                    "placeholder": (
                        "Conte brevemente seu momento profissional, "
                        "seus desafios e o que você deseja desenvolver."
                    ),
                    "rows": 7,
                }
            ),
        }


class CadastroAlunoForm(forms.Form):
    first_name = forms.CharField(
        max_length=150,
        label="Nome",
        widget=forms.TextInput(attrs={"placeholder": "Digite seu nome"}),
    )
    last_name = forms.CharField(
        max_length=150,
        label="Sobrenome",
        widget=forms.TextInput(attrs={"placeholder": "Digite seu sobrenome"}),
    )
    telefone = forms.CharField(
        max_length=30,
        label="Número",
        widget=forms.TextInput(attrs={"placeholder": "Digite seu telefone"}),
    )
    email = forms.EmailField(
        label="E-mail",
        widget=forms.EmailInput(attrs={"placeholder": "Digite seu e-mail"}),
    )
    password1 = forms.CharField(
        label="Senha",
        widget=forms.PasswordInput(attrs={"placeholder": "Crie uma senha"}),
    )
    password2 = forms.CharField(
        label="Confirmar senha",
        widget=forms.PasswordInput(attrs={"placeholder": "Confirme sua senha"}),
    )

    def clean_email(self):
        email = self.cleaned_data["email"].strip().lower()
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Já existe uma conta com este e-mail.")
        return email

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            self.add_error("password2", "As senhas não coincidem.")

        return cleaned_data

    def save(self):
        email = self.cleaned_data["email"].strip().lower()
        first_name = self.cleaned_data["first_name"].strip()
        last_name = self.cleaned_data["last_name"].strip()
        telefone = self.cleaned_data["telefone"].strip()
        password = self.cleaned_data["password1"]

        base_username = email.split("@")[0]
        username = base_username
        counter = 1

        while User.objects.filter(username=username).exists():
            username = f"{base_username}{counter}"
            counter += 1

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
        )

        PerfilAluno.objects.create(
            user=user,
            nome_exibicao=f"{first_name} {last_name}".strip(),
            telefone=telefone,
            acesso_ativo=False,
        )

        return user