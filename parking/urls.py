from django.urls import path
from . import views
from .views import cadastro_view, login_view, logout_view

urlpatterns= [
    path('', views.index, name='index'),
    path('home/', views.home_view, name='home'),
    path('vagas', views.vagas, name='vagas'),
    path('veiculos', views.veiculos, name='veiculos'),
    path('cadastro/', cadastro_view, name='cadastro'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    
]





