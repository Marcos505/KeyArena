from django.db import models

# Create your models here.

class Usuarios(models.Model):
    usu_id = models.AutoField(primary_key=True)
    usu_nome = models.TextField(max_length=150)
    usu_sobrenome = models.TextField(max_length=150)
    usu_data_nascimento = models.DateField()
    usu_celular = models.TextField(max_length=20)
    usu_email = models.TextField(max_length=150)
    usu_senha = models.TextField(max_length=150)

class Participant(models.Model):
    name = models.CharField(max_length=100)

class Stage(models.Model):
    name = models.CharField(max_length=100)
    tournament_id = models.IntegerField()
    type = models.CharField(max_length=50)
    seeding = models.JSONField()  # Armazenar a lista de seeding como JSON

class Match(models.Model):
    stage = models.ForeignKey(Stage, on_delete=models.CASCADE)
    participant1 = models.ForeignKey(Participant, related_name='matches_as_participant1', on_delete=models.CASCADE)
    participant2 = models.ForeignKey(Participant, related_name='matches_as_participant2', on_delete=models.CASCADE)
    winner = models.ForeignKey(Participant, related_name='matches_as_winner', null=True, blank=True, on_delete=models.SET_NULL)