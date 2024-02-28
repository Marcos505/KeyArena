from django.http import HttpResponse
from django.shortcuts import render


# Create your views here.
def login(request):
    return render(request, 'KeyArenaApp/pages/login.html')

def cadastro(request):
    return render(request, 'KeyArenaApp/pages/cadastro.html')

def home(request):
    return render(request, 'KeyArenaApp/pages/home.html')

