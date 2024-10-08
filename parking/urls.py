from django.urls import path
from . import views

urlpatterns= [
    path('', views.index, name='index'),
    path('home', views.home, name='home'),
    path('vagas', views.vagas, name='vagas'),
    path('veiculos', views.veiculos, name='veiculos'),
]
