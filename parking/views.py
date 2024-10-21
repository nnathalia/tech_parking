
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import ProprietarioForm, LoginForm
from .models import Proprietario, Veiculo



def cadastro_view(request):
    if request.method == 'POST':
        form = ProprietarioForm(request.POST)
        if form.is_valid():
            proprietario = form.save(commit=False)  # Não salva ainda
            senha = form.cleaned_data.get('senha')
            proprietario.set_password(senha)  # Hash da senha
            proprietario.save()  # Agora salva no banco com a senha hashada
            return redirect('login')
    else:
        form = ProprietarioForm()

    return render(request, 'auth/cadastro.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            cpf = form.cleaned_data.get('username')
            senha = form.cleaned_data.get('password')
            print(f"Tentando autenticar usuário com CPF: {cpf}")

            # Autentica com o CPF como username
            user = authenticate(request, username=cpf, password=senha)

            if user is not None:
                login(request, user)  # Isso atualiza automaticamente o campo last_login
                print(f"Login bem-sucedido para {user.nome}")
                return redirect('home')
            else:
                messages.error(request, "CPF ou senha inválidos.")
    else:
        form = LoginForm()

    return render(request, 'auth/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def home_view(request):
    # Pega o proprietário logado
    proprietario_logado = request.user

    # Passa o nome do proprietário para o contexto
    context = {
      'nome_proprietario': proprietario_logado.nome
    }
    return render(request, 'pages/home.html', context)



def index(request):
  """Página principal do Tech Parking"""
  return render(request, 'template/index.html')

@login_required
def veiculos(request):
  '''veiculo = Veiculo.objects.order_by('id')
  context = {'veiculo': veiculo}
  return render(request, 'parking/veiculos.html', context)'''
  return render(request, 'pages/veiculos.html')

@login_required
def vagas(request):
  return render(request, 'pages/vagas.html')

def index(request):
  return render(request, 'index.html')
