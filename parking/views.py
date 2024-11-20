import json
from django.shortcuts import render
from .models import Proprietario, Veiculo
from django.views.decorators.csrf import csrf_exempt

def index(request):
  """Página principal do Tech Parking"""
  return render(request, 'template/index.html')

def proprietario(request, proprietario_id):
  propritario = Proprietario.objects.get(id = proprietario_id)

@csrf_exempt
def veiculos(request):
  if request.method == 'POST':
    data = request.POST

    proprietario = Proprietario.objects.get(id=1) #TODO: Criar combobox para pegar o proprietário
    veiculo = Veiculo.objects.create(placa=data['placa'], modelo=data['modelo'], cor=data['cor'], proprietario=proprietario)

  veiculos = Veiculo.objects.all()

  return render(request, 'pages/veiculos.html', {'veiculos': veiculos})

def index(request):
  return render(request, 'index.html')

def home(request):
  return render(request, 'pages/home.html')

def vagas(request):
  return render(request, 'pages/vagas.html')

def login(request):
  return render(request, 'auth/login.html')

def cadastro(request):
  return render(request, 'auth/cadastro.html')

