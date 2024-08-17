from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages

from .models import Usuarios



# Create your views here.
def page_apresentation(request):
    return render(request, 'index.html')

def cadastro(request):
    if request.method == "GET":
        return render(request, 'cadastro.html')
    else:
        email = request.POST.get('email')
        senha = request.POST.get('senha')
        nome = request.POST.get('nome')
        sobrenome = request.POST.get('sobrenome')
        data_nascimento = request.POST.get('data_nascimento')
        celular = request.POST.get('celular')

        if email or senha or nome or sobrenome or data_nascimento or celular == '':
            #messages.error(request, 'Preencha todos os campos!')
            #return render(request, 'cadastro.html')
            return HttpResponse("Preencha todos os campos")
        else:
            user = Usuarios.objects.filter(usu_email = email).first()

            if user:
                messages.info(request, 'Email já cadastrado tente novamente!')
                return render(request, 'cadastro.html')
            else:

                novo_usuario = Usuarios()
                novo_usuario.usu_nome = nome
                novo_usuario.usu_sobrenome = sobrenome
                novo_usuario.usu_data_nascimento = data_nascimento
                novo_usuario.usu_celular = celular
                novo_usuario.usu_email = email
                novo_usuario.usu_senha = senha
                novo_usuario.save()

                messages.info(request, 'Você foi cadastrado com sucesso!')
                return redirect('/login')


def login(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    else:
        email = request.POST.get('email')
        senha = request.POST.get('senha')

        user_email = Usuarios.objects.filter(usu_email = email).first()
        user_senha = Usuarios.objects.filter(usu_senha = senha).first()

        if user_email and user_senha:
            return HttpResponse("Logado")
        else:
            messages.info(request, 'Email ou senha incorretos! Tente Novamente')
            return redirect('/login')
        
def home_page(request):
    return render(request, 'page_home.html')

def torneio(request):
    return render(request, 'criartorneio.html')