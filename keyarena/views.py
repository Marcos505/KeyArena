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

@login_required
def participar(request):
    usuario_da_sessao_id = request.user.id 
    torneios = Torneio.objects.exclude(tor_usu_criador_id=usuario_da_sessao_id)  

    return render(request, 'participar.html', {'torneios': torneios})

def sair(request):
    logout(request)
    return redirect('index')

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

    return render(request, 'inscricao.html', 
        {'torneio': torneio,
        'quant_participantes': num_participantes })

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
        return redirect('torneios')  # Redirecionar após cancelar

    return redirect('torneios.html')  # Redirecionar se não estava inscrito


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

        user = request.user  
        token = user.key_auth
        print(token)

        otp = pyotp.TOTP(token)
        code_right = otp.now()
        if codigo == code_right:
            return redirect('home_page')
        else:
            return redirect('qrcode_login')
    return redirect('home_page')