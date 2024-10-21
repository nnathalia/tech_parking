from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.hashers import check_password
from .models import Proprietario

class CPFBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            # Procurar o usuário pelo CPF
            user = Proprietario.objects.get(cpf=username)
        except Proprietario.DoesNotExist:
            return None

        # Verificar se a senha fornecida é válida
        if check_password(password, user.senha):
            return user
        return None

    def get_user(self, user_id):
        try:
            return Proprietario.objects.get(pk=user_id)
        except Proprietario.DoesNotExist:
            return None