from django.shortcuts import render
from . models import Proprietario, Veiculo

def index(request):
  """Página principal do Tech Parking"""
  return render(request, 'template/index.html')

def proprietario(request, proprietario_id):
  propritario = Proprietario.objects.get(id = proprietario_id)
  

def veiculo(request):
  veiculo = Veiculo.objects.order_by('id')
  context = {'veiculo': veiculo}
  return render(request, 'parking/veiculos.html', context)

def index(request):
  return render(request, 'index.html')

def home(request):
  return render(request, 'pages/home.html')

def vagas(request):
  return render(request, 'pages/vagas.html')

