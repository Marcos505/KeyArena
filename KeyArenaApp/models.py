from django.db import models
from django.core.validators import RegexValidator
from django.core.validators import MinValueValidator, MaxValueValidator


class User(models.Model):
    first_name = models.CharField(max_length=50, null=False, blank=False, validators=[RegexValidator(
                                    regex='^[A-Za-z]*$',
                                    message='O nome deve conter apenas letras.',
                                    code='invalid_name')])
    last_name = models.CharField(max_length=50, null=False, blank=False, validators=[RegexValidator(
                                    regex='^[A-Za-z]*$',
                                    message='O nome deve conter apenas letras.',
                                    code='invalid_name')])
    email = models.EmailField(default='')
    password = models.CharField(max_length=100, default='')
    administrator = models.BooleanField(default=False)

class Address(models.Model):
    municipality = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    neighborhood = models.CharField(max_length=50)
    street = models.CharField(max_length=50, validators=[RegexValidator(
                                    regex='^[A-Za-z]*$',
                                    message='A rua deve conter apenas números.',
                                    code='invalid_street')])
    number = models.CharField(max_length=20)
    cep = models.CharField(max_length=10, validators=[RegexValidator(
                                    regex='^[0-9]*$',
                                    message='A CEP deve conter apenas números.',
                                    code='invalid_cep')])
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)

class Format(models.Model):
    format_name = models.CharField(max_length=50, null=False, blank=False)

class Tournament(models.Model):
    name = models.CharField(max_length=50, null=False, blank=False)
    quantity_participants = models.IntegerField(null=False, blank=False, validators=[
                                    MinValueValidator(2, message="O torneio deve ter no mínimo 2 participantes."),
                                    MaxValueValidator(100, message="100 participantes, torneio lotado.")])
    format = models.ForeignKey(Format, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

