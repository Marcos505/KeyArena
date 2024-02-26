from django.urls import path
from KeyArenaApp.views import home, login, cadastro

urlpatterns = [
    path('', login),
    path('home', home),
    path('cadastro', cadastro)

]