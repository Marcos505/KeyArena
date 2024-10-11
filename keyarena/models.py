from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

class UsuarioManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('O email deve ser fornecido')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)  # Armazena a senha de forma segura
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, password, **extra_fields)

class Usuario(AbstractBaseUser, PermissionsMixin):
    usu_id = models.AutoField(primary_key=True)
    usu_nome_completo = models.CharField(max_length=255)
    usu_data_nascimento = models.DateField(null=True, blank=True)
    usu_telefone = models.CharField(max_length=255, null=True, blank=True)
    usu_nickname = models.CharField(max_length=25, null=True, blank=True)
    usu_email = models.EmailField(max_length=255, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    foto_perfil = models.ImageField(upload_to='fotos_perfil/', null=True, blank=True)

    objects = UsuarioManager()

    USERNAME_FIELD = 'usu_email'  # Usa o email como identificador
    REQUIRED_FIELDS = ['usu_nome_completo']  # Campos obrigatórios além do email

    def __str__(self):
        return self.usu_nome_completo
    
    @property
    def id(self):
        return self.usu_id

# Tabela: tipos_torneio
class TiposTorneio(models.Model):
    ttor_id = models.AutoField(primary_key=True)
    ttor_tipo = models.CharField(max_length=255)

    def __str__(self):
        return self.ttor_tipo

# Tabela: torneios
class Torneio(models.Model):
    tor_id = models.AutoField(primary_key=True)
    tor_nome_torneio = models.CharField(max_length=255)
    tor_quant_participantes = models.IntegerField()
    tor_ativo = models.BooleanField(default=True)
    tor_data_criacao = models.DateField(auto_now_add=True)
    tor_descricao = models.CharField(max_length=255)
    tor_usu_criador = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    tor_tipo_torneio = models.ForeignKey(TiposTorneio, on_delete=models.CASCADE)

    tor_data_inicio = models.DateField(null=True, blank=True)  
    tor_data_inicio_inscricao = models.DateField(null=True, blank=True)  
    tor_data_fim_inscricao = models.DateField(null=True, blank=True)  

    def __str__(self):
        return self.tor_nome_torneio

# Tabela: torneio_rodadas
class TorneioRodada(models.Model):
    rod_id = models.AutoField(primary_key=True)
    rod_tor_torneio = models.ForeignKey(Torneio, on_delete=models.CASCADE)
    rod_rodada = models.IntegerField()

    def __str__(self):
        return f"Torneio {self.rod_tor_torneio} - Rodada {self.rod_rodada}"

# Tabela: inscricao_torneio
class InscricaoTorneio(models.Model):
    ins_id = models.AutoField(primary_key=True)
    ins_tor_torneios = models.ForeignKey('Torneio', on_delete=models.CASCADE)
    ins_usu_participante = models.ForeignKey('Usuario', on_delete=models.CASCADE)

    def __str__(self):
        return f"Inscrição de {self.ins_usu_participante} no Torneio {self.ins_tor_torneios}"

# Tabela: partidas_rodada
class PartidaRodada(models.Model):
    par_id = models.AutoField(primary_key=True)
    par_rod_rodada = models.ForeignKey(TorneioRodada, on_delete=models.CASCADE)
    par_usu_participante_um = models.ForeignKey(Usuario, related_name='partida_participante_um', on_delete=models.CASCADE)
    par_usu_participante_dois = models.ForeignKey(Usuario, related_name='partida_participante_dois', on_delete=models.CASCADE)
    par_resultado = models.BooleanField()

    def __str__(self):
        return f"Partida entre {self.par_usu_participante_um} e {self.par_usu_participante_dois}"

# Tabela: resultados
class Resultado(models.Model):
    res_id = models.AutoField(primary_key=True)
    res_tor_torneio = models.ForeignKey(Torneio, on_delete=models.CASCADE)
    res_usu_participante = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    res_resultado = models.IntegerField()

    def __str__(self):
        return f"Resultado de {self.res_usu_participante} no Torneio {self.res_tor_torneio}: {self.res_resultado}"