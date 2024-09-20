from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages

def index(request):
    return render(request, 'index.html')

def cadastro(request):
    return render(request, 'cadastro.html')

def home_page(request):
    return render(request, 'page_home.html')

def torneio(request):
    return render(request, 'criartorneio.html')

def torneio2(request):
    return render(request, 'criartorneio2.html')
