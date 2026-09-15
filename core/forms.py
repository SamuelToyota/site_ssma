from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password

from .models import MentoriaContato, NewsletterLead, PerfilAluno


class HoneypotMixin:
    def clean_website(self):
        value = self.cleaned_data.get("website", "")
        if value:
            raise forms.ValidationError("Não foi possível enviar o formulário.")
        return value


class BaseContatoForm(HoneypotMixin, forms.ModelForm):
    website = forms.CharField(
        required=False,
        label="Deixe este campo vazio",
        widget=forms.TextInput(
            attrs={"tabindex": "-1", "autocomplete": "off", "aria-hidden": "true"}
        ),
    )
    consentimento = forms.BooleanField(
        required=True,
        label="Li e concordo com a Política de Privacidade.",
    )

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.consentimento_privacidade = True
        if commit:
            instance.save()
        return instance


class ContatoForm(BaseContatoForm):
    class Meta:
        model = MentoriaContato
        fields = [
            "nome",
            "email",
            "telefone",
            "tipo_interesse",
            "empresa",
            "cargo",
            "mensagem",
        ]
        labels = {
            "nome": "Nome completo",
            "email": "E-mail",
            "telefone": "Telefone (opcional)",
            "tipo_interesse": "Assunto",
            "empresa": "Empresa (opcional)",
            "cargo": "Cargo (opcional)",
            "mensagem": "Como podemos ajudar?",
        }
        widgets = {
            "nome": forms.TextInput(attrs={"autocomplete": "name"}),
            "email": forms.EmailInput(attrs={"autocomplete": "email"}),
            "telefone": forms.TextInput(attrs={"autocomplete": "tel"}),
            "empresa": forms.TextInput(attrs={"autocomplete": "organization"}),
            "cargo": forms.TextInput(attrs={"autocomplete": "organization-title"}),
            "mensagem": forms.Textarea(
                attrs={
                    "placeholder": "Conte brevemente o contexto e o que você procura.",
                    "rows": 6,
                }
            ),
        }


class MentoriaContatoForm(BaseContatoForm):
    class Meta:
        model = MentoriaContato
        fields = ["nome", "email", "telefone", "mensagem"]
        labels = {
            "nome": "Nome completo",
            "email": "E-mail",
            "telefone": "Telefone (opcional)",
            "mensagem": "O que você deseja desenvolver?",
        }
        widgets = {
            "nome": forms.TextInput(attrs={"autocomplete": "name"}),
            "email": forms.EmailInput(attrs={"autocomplete": "email"}),
            "telefone": forms.TextInput(attrs={"autocomplete": "tel"}),
            "mensagem": forms.Textarea(attrs={"rows": 6}),
        }

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.tipo_interesse = "mentoria"
        if commit:
            instance.save()
        return instance


class EmpresaContatoForm(BaseContatoForm):
    class Meta:
        model = MentoriaContato
        fields = ["nome", "empresa", "cargo", "email", "telefone", "mensagem"]
        labels = {
            "nome": "Nome completo",
            "empresa": "Empresa",
            "cargo": "Cargo",
            "email": "E-mail corporativo",
            "telefone": "Telefone (opcional)",
            "mensagem": "Qual desafio sua organização quer trabalhar?",
        }
        widgets = {
            "nome": forms.TextInput(attrs={"autocomplete": "name"}),
            "empresa": forms.TextInput(attrs={"autocomplete": "organization"}),
            "cargo": forms.TextInput(attrs={"autocomplete": "organization-title"}),
            "email": forms.EmailInput(attrs={"autocomplete": "email"}),
            "telefone": forms.TextInput(attrs={"autocomplete": "tel"}),
            "mensagem": forms.Textarea(attrs={"rows": 6}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["empresa"].required = True
        self.fields["cargo"].required = True

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.tipo_interesse = "treinamento_empresa"
        if commit:
            instance.save()
        return instance


class NewsletterLeadForm(HoneypotMixin, forms.ModelForm):
    website = forms.CharField(
        required=False,
        label="Deixe este campo vazio",
        widget=forms.TextInput(
            attrs={"tabindex": "-1", "autocomplete": "off", "aria-hidden": "true"}
        ),
    )
    consentimento = forms.BooleanField(
        required=True,
        label="Aceito receber conteúdos e posso cancelar a qualquer momento.",
    )

    class Meta:
        model = NewsletterLead
        fields = ["nome", "email"]
        labels = {"nome": "Nome", "email": "E-mail"}
        widgets = {
            "nome": forms.TextInput(attrs={"autocomplete": "name"}),
            "email": forms.EmailInput(attrs={"autocomplete": "email"}),
        }

    def validate_unique(self):
        # Uma nova inscrição com o mesmo e-mail reativa o cadastro existente.
        return


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

        if password1:
            user = User(
                username=self.cleaned_data.get("email", ""),
                email=self.cleaned_data.get("email", ""),
                first_name=self.cleaned_data.get("first_name", ""),
                last_name=self.cleaned_data.get("last_name", ""),
            )
            try:
                validate_password(password1, user=user)
            except forms.ValidationError as error:
                self.add_error("password1", error)

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
