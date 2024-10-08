from django.db import models

# Tabela: usuario
class Usuario(models.Model):
    usu_id = models.AutoField(primary_key=True)
    usu_nome_completo = models.CharField(max_length=255)
    usu_data_nascimento = models.DateField(null=True, blank=True)
    usu_telefone = models.CharField(max_length=255, null=True, blank=True)
    usu_nickname = models.CharField(max_length=25, null=True, blank=True)
    usu_email = models.EmailField(max_length=255, unique=True)
    usu_senha = models.CharField(max_length=255)
    usu_tipo_usuario = models.CharField(max_length=20)

    def _str_(self):
        return self.usu_nome_completo

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
    tor_modalidade = models.CharField(max_length=50)
    tor_data_criacao = models.DateField(auto_now_add=True)
    tor_descricao = models.CharField(max_length=255)
    tor_usu_criador = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    tor_tipo_torneio = models.ForeignKey(TiposTorneio, on_delete=models.CASCADE)

    def _str_(self):
        return self.tor_nome_torneio

# Tabela: torneio_rodadas
class TorneioRodada(models.Model):
    rod_id = models.AutoField(primary_key=True)
    rod_tor_torneio = models.ForeignKey(Torneio, on_delete=models.CASCADE)
    rod_rodada = models.IntegerField()

    def _str_(self):
        return f"Torneio {self.rod_tor_torneio} - Rodada {self.rod_rodada}"

# Tabela: inscricao_torneio
class InscricaoTorneio(models.Model):
    ins_id = models.AutoField(primary_key=True)
    ins_tor_torneios = models.ForeignKey(Torneio, on_delete=models.CASCADE)
    ins_usu_participante = models.ForeignKey(Usuario, on_delete=models.CASCADE)

    def _str_(self):
        return f"Inscrição de {self.ins_usu_participante} no Torneio {self.ins_tor_torneios}"

# Tabela: partidas_rodada
class PartidaRodada(models.Model):
    par_id = models.AutoField(primary_key=True)
    par_rod_rodada = models.ForeignKey(TorneioRodada, on_delete=models.CASCADE)
    par_usu_participante_um = models.ForeignKey(Usuario, related_name='partida_participante_um', on_delete=models.CASCADE)
    par_usu_participante_dois = models.ForeignKey(Usuario, related_name='partida_participante_dois', on_delete=models.CASCADE)
    par_resultado = models.BooleanField()

    def _str_(self):
        return f"Partida entre {self.par_usu_participante_um} e {self.par_usu_participante_dois}"

# Tabela: resultados
class Resultado(models.Model):
    res_id = models.AutoField(primary_key=True)
    res_tor_torneio = models.ForeignKey(Torneio, on_delete=models.CASCADE)
    res_usu_participante = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    res_resultado = models.IntegerField()

    def _str_(self):
        return f"Resultado de {self.res_usu_participante} no Torneio {self.res_tor_torneio}: {self.res_resultado}"