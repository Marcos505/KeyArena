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