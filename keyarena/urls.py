from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('cadastro/', views.cadastro, name='cadastro'),
    path('home_page/', views.home_page, name='home_page'),
    path('torneios/', views.entrartorneio, name='torneios'),
    
    path('perfil/', views.perfil, name='perfil'),
    path('perfil/', views.editar_perfil, name='editar_perfil'),

    path('participar/', views.participar, name='participar'),
    path('criar/', views.salvar_torneio1, name='salvar_torneio1'),
    path('criar/etapa2/', views.salvar_torneio2, name='salvar_torneio2'),

    path('sair/', views.sair, name='sair')
]
