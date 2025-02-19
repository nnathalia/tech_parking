from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse, StreamingHttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Monitoramento, Veiculo, Vaga
import json
import time
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.utils.timezone import now



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
    
    if len(password) < 6:
      messages.error(request, 'A senha precisa ter no mínimo 6 caracters')
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
def perfil(request):
  return render(request, 'pages/perfil.html')

@login_required(login_url='login')
def veiculos(request):
  return render(request, 'pages/veiculos.html')

@login_required(login_url='login')
@csrf_exempt
def veiculos(request):
    if request.method == 'POST':
        data = request.POST
        placa = data['placa'].upper()  # Normaliza a placa para evitar duplicações por letras minúsculas
        modelo = data['modelo']
        cor = data['cor']

        # Verifica se a placa já existe no banco de dados
        if Veiculo.objects.filter(placa=placa).exists():
            messages.error(request, "Esta placa já está cadastrada!")
        else:
            Veiculo.objects.create(
                placa=placa,
                modelo=modelo,
                cor=cor,
                proprietario=request.user
            )
            messages.success(request, "Veículo cadastrado com sucesso!")

    # Filtrar os veículos do usuário logado
    veiculos = Veiculo.objects.filter(proprietario=request.user)

    return render(request, 'pages/veiculos.html', {'veiculos': veiculos})


@login_required(login_url='login')
def vagas(request):
  vagas = Vaga.objects.all()
  # Se a requisição for AJAX, retorna apenas o fragmento
  if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
    return render(request, 'status_fragment.html', {'vagas': vagas})

    # Caso contrário, retorna a página completa
  return render(request, 'pages/vagas.html', {'vagas': vagas})

def index(request):
  return render(request, 'index.html')


def handler404(request, exception):
  return render(request, 'errors/404.html')


def atualizar_status(self, distancia):
    print(f"Atualizando status da vaga {self.vaga.codigo_vaga} com distância {distancia} cm")  # Debug
    
    if distancia < 10:  
        self.status_vaga = "Ocupada"
        self.vaga.ocupada = True
    else:
        self.status_vaga = "Disponível"
        self.vaga.ocupada = False

    print(f"Novo status: {self.status_vaga}")  # Debug

    self.vaga.save()
    self.save()



@csrf_exempt
def atualizar_monitoramento(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            distancia = data.get("distancia")
            codigo_vaga = data.get("codigo_vaga")  

            vaga = Vaga.objects.get(codigo_vaga=codigo_vaga)

            # Criar uma nova instância de Monitoramento
            monitoramento = Monitoramento(vaga=vaga, data_hora=now())
            
            # Atualizar status baseado na distância
            monitoramento.atualizar_status(distancia)

            return JsonResponse({"mensagem": "Status atualizado com sucesso!"}, status=200)
        except Vaga.DoesNotExist:
            return JsonResponse({"erro": "Vaga não encontrada"}, status=404)
        except Exception as e:
            return JsonResponse({"erro": str(e)}, status=400)

    return JsonResponse({"erro": "Método não permitido"}, status=405)
  
  
def verificar_status_vaga(request, codigo_vaga):
    try:
        vaga = Vaga.objects.get(codigo_vaga=codigo_vaga)
        return JsonResponse({"ocupada": vaga.ocupada})
    except Vaga.DoesNotExist:
        return JsonResponse({"erro": "Vaga não encontrada"}, status=404)
      
def monitorar_vaga(request, codigo_vaga):
    def evento():
        while True:
            try:
                vaga = Vaga.objects.get(codigo_vaga=codigo_vaga)
                status = "Ocupada" if vaga.ocupada else "Disponível"
                yield f"data: {status}\n\n"
                time.sleep(10)  # Atualiza a cada 10 segundos
            except Vaga.DoesNotExist:
                yield "data: Vaga não encontrada\n\n"
                break

    response = StreamingHttpResponse(evento(), content_type='text/event-stream')
    response['Cache-Control'] = 'no-cache'
    return response
  