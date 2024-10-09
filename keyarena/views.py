from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import TiposTorneio
from keyarena.models import Torneio

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


def modalidade_dinamica(request):
    modalidades = TiposTorneio.objects.all()
    return render(request, 'criartorneio.html', {'modalidades': modalidades})

def salvar_torneio1(request):
    if request.method == 'POST':
        nome_torneio = request.POST.get('tournament-name')
        modalidade_id = request.POST.get('modality')
        quant_participants = request.POST.get('tournament-max-player')
        descricao = request.POST.get('description')
        # usuario_criador = request.user

        request.session['nome_torneio'] = nome_torneio
        request.session['modalidade_id'] = modalidade_id
        request.session['quant_participants'] = quant_participants
        request.session['descricao'] = descricao
        # request.session['usuario_criador'] = usuario_criador

        return redirect(salvar_torneio2)

    return render(request, 'criartorneio.html')


def salvar_torneio2(request):
    if request.method == 'POST':
        data_inicio_torneio = request.POST.get('start-date')
        data_inicio_inscricao = request.POST.get('registration-start')
        data_fim_inscricao = request.POST.get('registration-end')
        
        
        # Recuperar os dados armazenados na sessão da primeira etapa
        nome_torneio = request.session.get('nome_torneio')
        modalidade_id = request.session.get('modalidade_id')
        quant_participants = request.session.get('quant_participants')
        descricao = request.session.get('descricao')
        # usuario_criador = request.user  # Assumindo que o usuário está autenticado

        # Buscar a modalidade (TiposTorneio) pelo ID
        modalidade = TiposTorneio.objects.get(ttor_id=modalidade_id)

        torneio = Torneio(
            tor_nome_torneio=nome_torneio,
            tor_quant_participantes=quant_participants,
            tor_descricao=descricao,
            # tor_usu_criador=usuario_criador,
            tor_tipo_torneio=modalidade,
            tor_data_inicio=data_inicio_torneio,
            tor_data_fim_inscricao=data_fim_inscricao,
            tor_data_inicio_inscricao=data_inicio_inscricao,
        )

        torneio.save()

        # Limpar os dados da sessão após salvar
        request.session.flush()

        messages.success(request, 'Torneio criado com sucesso!')
        return redirect('home_page')

    # Renderizar o formulário da segunda etapa
    return render(request, 'criartorneio2.html')

def entrartorneio(request):
    torneios = Torneio.objects.all()

    return render(request, 'torneios.html', {'torneios': torneios})

def profile(request):
    return render(request, 'perfil.html')
  
