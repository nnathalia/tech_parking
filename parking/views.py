from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Veiculo, Vaga


def cadastro (request):
  if request.method == "GET":
    return render(request, 'auth/cadastro.html')
  else:
    first_name = request.POST.get('first_name')
    last_name = request.POST.get('last_name')
    username = request.POST.get('username')
    email = request.POST.get('email')
    password = request.POST.get('password')
    confirm_password = request.POST.get('confirm_password')
    
    email_exists = User.objects.filter(email=email).exists()
    if email_exists:
      messages.error(request, 'Este email ja foi cadastrado!')
      return render(request, 'auth/cadastro.html')
    
    user_exists = User.objects.filter(username=username).exists()
    if user_exists:
      messages.error(request, 'Já existe um usuário com este username')
      return render(request, 'auth/cadastro.html')
        
    if password != confirm_password:
      messages.error(request, 'As senhas não coincidem.')
      return render(request, 'auth/cadastro.html')
    
    if len(password) < 8:
      messages.error(request, 'A senha precisa ter no mínimo 8 caracters')
      return render(request, 'auth/cadastro.html')
    
    user = User.objects.create_user(username=username, email=email, password=password, first_name=first_name, last_name= last_name)
    user.save
    return redirect('login')
    
    
def login_view (request):
  if request.method == "GET":
    return render(request, 'auth/login.html')
  else:
    username = request.POST.get('username') 
    password = request.POST.get('password')
    
    user = authenticate(username=username, password=password)
    
    if user:
      login(request, user )
      
      return redirect('home')
    else:
      messages.error(request, 'Usuário ou senha incorretos!')
      return render(request, 'auth/login.html')
    

def logout_view(request):
  logout(request)
  return redirect('index')
  
@login_required(login_url='login')
def home(request):
  return render(request, 'pages/home.html')

@login_required(login_url='login')
def veiculos(request):
  return render(request, 'pages/veiculos.html')

@login_required(login_url='login')
def vagas(request):
  return render(request, 'pages/vagas.html')

def index(request):
  return render(request, 'index.html')


def handler404(request, exception):
  return render(request, 'errors/404.html')