from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend


class EmailOrUsernameModelBackend(ModelBackend):
    """Permite entrar com o e-mail cadastrado ou com o nome de usuário legado."""

    def authenticate(self, request, username=None, password=None, **kwargs):
        UserModel = get_user_model()
        login_value = username or kwargs.get(UserModel.USERNAME_FIELD)

        if login_value is None or password is None:
            return None

        try:
            if "@" in login_value:
                user = UserModel._default_manager.get(email__iexact=login_value.strip())
            else:
                user = UserModel._default_manager.get_by_natural_key(login_value)
        except (UserModel.DoesNotExist, UserModel.MultipleObjectsReturned):
            # Mantém o custo de hash semelhante quando o usuário não existe.
            UserModel().set_password(password)
            return None

        if user.check_password(password) and self.user_can_authenticate(user):
            return user
        return None
