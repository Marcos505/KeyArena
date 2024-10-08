from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('cadastro/', views.cadastro, name='cadastro'),
    path('home_page/', views.home_page, name='home_page'),
    path('criar/', views.torneio, name='torneio'),
    path('criar1/', views.torneio2, name='torneio2'),
    path('torneios/', views.entrartorneio, name='torneios'),
    path('perfil/', views.profile, name='perfil')
]
