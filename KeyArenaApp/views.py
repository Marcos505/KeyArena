from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def login(request):
    return render(request, 'KeyArenaApp/login.html')

def cadastro(request):
    return render(request, 'KeyArenaApp/cadastro.html')

def home(request):
    return render(request, 'KeyArenaApp/home.html')

