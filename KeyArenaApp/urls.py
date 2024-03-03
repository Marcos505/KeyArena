from django.urls import path
from KeyArenaApp.views import home, login, cadastro, salvar

urlpatterns = [
    path('', login),
    path('home', home),
    path('cadastro', cadastro),
    path('salvar', salvar, name='salvar')

]