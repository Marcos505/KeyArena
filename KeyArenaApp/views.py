from django.http import HttpResponse
from django.shortcuts import render
from .models import User


# Create your views here.
def login(request):
    return render(request, 'KeyArenaApp/pages/login.html')

def cadastro(request):
    return render(request, 'KeyArenaApp/pages/cadastro.html')

def home(request):
    return render(request, 'KeyArenaApp/pages/home.html')

def salvar(request):
    if request.method == 'POST':
        vfirt_name = request.POST.get("name")
        vlast_name = request.POST.get("sobrenome")
        vemail = request.POST.get("email")
        vsenha = request.POST.get("senha")
        administrador = False
        User.objects.create(first_name = vfirt_name, last_name = vlast_name, email = vemail, password = vsenha, administrator = administrador)
        return render(request, 'KeyArenaApp/pages/cadastro.html')
    else:
        return render(request, 'KeyArenaApp/pages/login.html')
    