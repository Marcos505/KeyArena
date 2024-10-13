from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import InscricaoTorneio, TiposTorneio, Usuario
from keyarena.models import Torneio
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required

def index(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)  # Autentica o usuário na sessão
            return redirect('home_page')
        else:
            messages.error(request, "Credenciais inválidas. Tente novamente.")  # Mensagem de erro
    else:
        form = AuthenticationForm()
    
    return render(request, 'index.html', {'form': form})

def cadastro(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        nome = request.POST.get('nome')
        sobrenome = request.POST.get('sobrenome')
        data_nascimento = request.POST.get('data_nascimento')
        celular = request.POST.get('celular')
        
        usuario = Usuario(
            usu_email=email,
            usu_nome_completo=f"{nome} {sobrenome}",
            usu_data_nascimento=data_nascimento,
            usu_telefone=celular
        )
        usuario.set_password(password)
        usuario.save()

        messages.success(request, 'Cadastro realizado com sucesso!')
        return redirect('index')
    
    return render(request, 'cadastro.html')

def home_page(request):
    usuario = request.user
    return render(request, 'page_home.html', {'usuario': usuario})

def salvar_torneio1(request):
    modalidades = TiposTorneio.objects.all()
    if request.method == 'POST':
        nome_torneio = request.POST.get('tournament-name')
        modalidade_id = request.POST.get('modality')
        quant_participants = request.POST.get('tournament-max-player')
        descricao = request.POST.get('description')
        usuario_criador_id = request.user.id  # Armazena apenas o ID do usuário

        request.session['nome_torneio'] = nome_torneio
        request.session['modalidade_id'] = modalidade_id
        request.session['quant_participants'] = quant_participants
        request.session['descricao'] = descricao
        request.session['usuario_criador_id'] = usuario_criador_id  # Salva apenas o ID

        return redirect('salvar_torneio2')

    return render(request, 'criartorneio.html', {'modalidades': modalidades})

def salvar_torneio2(request):
    if request.method == 'POST':
        data_inicio_torneio = request.POST.get('start-date')
        data_inicio_inscricao = request.POST.get('registration-start')
        data_fim_inscricao = request.POST.get('registration-end')
        
        nome_torneio = request.session.get('nome_torneio')
        modalidade_id = request.session.get('modalidade_id')
        quant_participants = request.session.get('quant_participants')
        descricao = request.session.get('descricao')

        usuario_criador_id = request.session.get('usuario_criador_id')

        if not usuario_criador_id:
            messages.error(request, "Usuário criador não encontrado.")
            return redirect('salvar_torneio1')  # Volta para a primeira etapa

        usuario_criador = Usuario.objects.get(usu_id=usuario_criador_id)

        modalidade = TiposTorneio.objects.get(ttor_id=modalidade_id)

        torneio = Torneio(
            tor_nome_torneio=nome_torneio,
            tor_quant_participantes=quant_participants,
            tor_descricao=descricao,
            tor_usu_criador=usuario_criador,
            tor_tipo_torneio=modalidade,
            tor_data_inicio=data_inicio_torneio,
            tor_data_fim_inscricao=data_fim_inscricao,
            tor_data_inicio_inscricao=data_inicio_inscricao,
        )

        torneio.save()

        request.session.flush()

        messages.success(request, 'Torneio criado com sucesso!')
        return redirect('home_page')

    return render(request, 'criartorneio2.html')

@login_required
def entrartorneio(request):
    usuario = request.user

    torneios = Torneio.objects.all()
    torneios = Torneio.objects.filter(tor_usu_criador=usuario)

    inscricoes = InscricaoTorneio.objects.filter(ins_usu_participante=usuario)

    return render(request, 'torneios.html', {'torneios': torneios, 'inscricoes': inscricoes})

@login_required
def perfil(request):
    usuario = request.user
    if request.method == 'POST':
        usuario.usu_nome_completo = request.POST.get('nome')
        usuario.usu_data_nascimento = request.POST.get('data_nascimento')
        usuario.usu_email = request.POST.get('email')
        usuario.usu_nickname = request.POST.get('nickname')
        usuario.usu_telefone = request.POST.get('telefone')
        

        if request.FILES.get('foto_perfil'):
            usuario.foto_perfil = request.FILES['foto_perfil']
            
        usuario.save()
        return redirect('perfil')
    
    return render(request, 'perfil.html', {'usuario': usuario})

def participar(request):
    usuario_da_sessao_id = request.user.id 
    torneios = Torneio.objects.exclude(tor_usu_criador_id=usuario_da_sessao_id)  

    return render(request, 'participar.html', {'torneios': torneios})

def sair(request):
    logout(request)
    return redirect('index')

def inscricao(request, torneio_id):
    torneio = Torneio.objects.get(tor_id=torneio_id)

    if request.method == 'POST':
        inscricao_existente = InscricaoTorneio.objects.filter(
            ins_usu_participante=request.user,
            ins_tor_torneios=torneio
        ).first()

        if inscricao_existente:
            
            return render(request, 'inscricao.html', {
                'torneio': torneio,
                'mensagem': 'Você já está inscrito neste torneio.'
            })

        inscricao = InscricaoTorneio()
        inscricao.ins_tor_torneios = torneio
        inscricao.ins_usu_participante = request.user 
        inscricao.save() 

        return render(request, 'inscricao.html', {'torneio': torneio})

    return render(request, 'inscricao.html', {'torneio': torneio})
