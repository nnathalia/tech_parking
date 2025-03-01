from django.urls import path
from . import views

urlpatterns= [
    path('', views.index, name='index'),
    path('cadastro', views.cadastro, name='cadastro'),
    path('login', views.login_view, name='login'),
    path('logout', views.logout_view, name='logout'),
    path('perfil', views.perfil, name='perfil'),
    path('home', views.home, name='home'),
    path('vagas', views.vagas, name='vagas'),
    path('veiculos', views.veiculos, name='veiculos'),
    path('api/atualizar_monitoramento/', views.atualizar_monitoramento, name='atualizar_monitoramento'),
]





