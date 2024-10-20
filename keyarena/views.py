from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from io import BytesIO
import pyotp
import qrcode
import base64
from .models import InscricaoTorneio, TiposTorneio, Usuario
from keyarena.models import Torneio
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.db.models import Count


from keyarena import models

def index(request):
    if hasattr(request.user, 'usu_id'):
        return redirect('home_page/') 

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            print(f'Usuário {user.usu_email} logado com sucesso.')
            if user.first_login:
                return redirect('qrcode_login')
            return redirect('qrcode_auth')
        else:
            messages.error(request, "Credenciais inválidas. Tente novamente.")
    else:
        form = AuthenticationForm()
    
    return render(request, 'index.html', {'form': form})

def cadastro(request):
    if hasattr(request.user, 'usu_id'):
        return redirect('home_page/')
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

@never_cache
@login_required
def home_page(request):
    usuario = request.user
    return render(request, 'page_home.html', {'usuario': usuario})

@never_cache
@login_required
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

@never_cache
@login_required
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


        messages.success(request, 'Torneio criado com sucesso!')
        return redirect('home_page')

    return render(request, 'criartorneio2.html')

@never_cache
@login_required
def entrartorneio(request):
    usuario = request.user

    torneios = Torneio.objects.filter(tor_usu_criador=usuario)

    inscricoes = InscricaoTorneio.objects.filter(ins_usu_participante=usuario)
    show_inscricoes = request.GET.get('from_participar', 'false') == 'true'

    return render(request, 'torneios.html', {
        'torneios': torneios, 
        'inscricoes': inscricoes,
        'show_inscricoes': show_inscricoes})

@never_cache
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


@never_cache
@login_required
def participar(request):
    usuario = request.user.id 
    torneios = Torneio.objects.exclude(tor_usu_criador_id=usuario).annotate(num_inscritos=Count('inscricaotorneio'))
    inscricoes = InscricaoTorneio.objects.filter(ins_usu_participante=usuario)  
    inscricoes_dict = {ins.ins_tor_torneios.tor_id: ins for ins in inscricoes}

    return render(request, 'participar.html', {
        'torneios': torneios,
        'inscricoes': inscricoes,
        'inscricoes_dict': inscricoes_dict
    })

def sair(request):
    logout(request)
    return redirect('index')

@never_cache
@login_required
def inscricao(request, torneio_id):
    torneio = Torneio.objects.get(tor_id=torneio_id)
    num_participantes = torneio.tor_quant_participantes

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

        return render(request, 'inscricao.html', {
            'torneio': torneio,
            'quant_participantes':num_participantes })

    return render(request, 'participar.html', 
        {'torneio': torneio,
        'quant_participantes': num_participantes })

@never_cache
@login_required
def cancelar_inscricao(request, torneio_id):
    torneio = Torneio.objects.get(tor_id=torneio_id)

    inscricao_existente = InscricaoTorneio.objects.filter(
        ins_usu_participante=request.user,
        ins_tor_torneios=torneio
    ).first()

    if inscricao_existente:
        inscricao_existente.delete()
        print('perdeu por K.O')
        return redirect('torneios')

    return redirect('torneios') 



def qrcode_login(request):
    user = request.user  
    token = user.generate_2fa_token()  
    email_user = user.usu_email

    link = pyotp.totp.TOTP(token).provisioning_uri(issuer_name='keyarena', name=email_user)

    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(link)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")

    buffer = BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0)

    img_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')


    return render(request, 'qrcode_login.html', {'img_base64': img_base64})


def validacao_otp(request):
    if request.method == 'POST':
        codigo = request.POST.get('codigo')
        
        try:
            user = request.user  
            token = user.key_auth
            mudar_senha = False
        except:
            email = request.POST.get('email')
            print(email)
            user = Usuario.objects.filter(usu_email=email).first()
            token = user.key_auth
            mudar_senha = True
        otp = pyotp.TOTP(token)
        code_right = otp.now()

        if codigo == code_right:
            if mudar_senha:
                return render(request,'mudar_senha.html',{'email':email})
            if user.first_login:
                user.first_login = 'False'  
                user.save()  
            return redirect('home_page')
        else:
            if user.first_login:

                return redirect('qrcode_login')
            elif mudar_senha:
                return render(request, 'qrcode_auth.html', {'email': email})
            else: 
                return redirect('qrcode_auth')


def qrcode_auth(request):
    return render(request, 'qrcode_auth.html')

def esqueci_senha(request):
    if hasattr(request.user, 'usu_id'):
        return redirect('home_page/') 
    return render(request, 'esqueci_senha.html')


def mudar_senha(request):
    email = request.POST.get('email')
    if email:
        try:
            user = Usuario.objects.filter(usu_email=email).first()
            if user.key_auth:
                return render(request,'qrcode_auth.html',{'email':user.usu_email})
        except Exception as e:
            return redirect('index')
        

def troca_senha(request):
    email = request.POST.get('email')
    password = request.POST.get('senha1')
    usuario = Usuario.objects.filter(usu_email=email).first()

    usuario.set_password(password)
    usuario.save()
    return redirect('/')

def page_not_found_view(request, exception):
    return redirect('/')



def chaveamento(request, torneio_id):
    torneio = Torneio.objects.get(tor_id=torneio_id)
    editable = request.GET.get('editable', 'true') == 'true'

    inscricoes = InscricaoTorneio.objects.filter(ins_tor_torneios=torneio)
    participantes = [ins.ins_usu_participante.usu_nome_completo for ins in inscricoes]

    return render(request, 'inscricao.html',{
        'torneio': torneio,
        'editable': editable,
        'participantes': participantes,})