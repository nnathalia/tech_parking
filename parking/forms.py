from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import Proprietario
from .utils import valida_cpf  # Importa a função de validação de CPF que criamos

class ProprietarioForm(forms.ModelForm):
    senha = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control', 
            'placeholder': '********'
        })
    )
    confirmar_senha = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control', 
            'placeholder': '********'
        })
    )

    class Meta:
        model = Proprietario
        fields = ['nome', 'cpf', 'telefone', 'email', 'tipo_prop']
        widgets = {
            'nome': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'ex.: Filipe Maciel Lopes'
            }),
            'cpf': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': '000.000.000-00'
            }),
            'telefone': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': '(XX) XXXXX-XXXX'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control', 
                'placeholder': 'exemplo@gmail.com'
            }),
            'tipo_prop': forms.Select(attrs={
                'class': 'form-select',
                'placeholder': 'Clique aqui para selecionar uma opção'
            })
        }

    def clean_cpf(self):
        cpf = self.cleaned_data.get('cpf')
        if not valida_cpf(cpf):
            raise forms.ValidationError("CPF inválido.")
        return cpf

    def clean_confirmar_senha(self):
        senha = self.cleaned_data.get('senha')
        confirmar_senha = self.cleaned_data.get('confirmar_senha')
        if senha != confirmar_senha:
            raise forms.ValidationError("As senhas não coincidem.")
        return confirmar_senha

class LoginForm(AuthenticationForm):
    username = forms.CharField(
        label="CPF", 
        widget=forms.TextInput(attrs={
            'autofocus': True, 
            'class': 'form-control',  # Classe CSS do frontend
            'placeholder': 'Digite seu CPF'  # Placeholder personalizado
        })
    )
    
    password = forms.CharField(
        label="Senha", 
        strip=False,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',  # Classe CSS do frontend
            'placeholder': 'Digite sua senha'  # Placeholder personalizado
        })
    )