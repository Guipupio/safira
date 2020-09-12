from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.utils.translation import gettext_lazy as _

# Adicionar Idade; sexo; Renda; Telefone
class Cliente(models.Model):
    class sexo_choices(models.TextChoices):
        MASCULINO = 'M', _("Masculino")
        FEMININO = "F", _("Feminino")


    id = models.BigAutoField(primary_key=True, unique=True)
    nome = models.CharField("Nome Completo", max_length=128)
    email = models.EmailField("Email")
    renda = models.FloatField("Renda Mensal")
    telefone = models.CharField("Telefone", max_length=14)
    data_nascimento = models.DateField("Data de Nascimento")
    sexo = models.CharField("Sexo", choices=sexo_choices.choices, max_length=32)


class Transacao(models.Model):
    id = models.BigAutoField(primary_key=True, unique=True)
    cliente = models.ForeignKey("Cliente", on_delete=models.PROTECT, verbose_name="Cliente")
    data  = models.DateTimeField("Data da Transação", blank=False, null=False)
    valor = models.FloatField("Valor")
    tipo = models.CharField("Indicador Crédito / Débito", max_length=128)
    informacoes = models.CharField("Detalhamento da Transação", max_length=512)
    saldo_conta = models.FloatField("Saldo Remanescente")
