# Generated by Django 3.1.1 on 2020-09-12 22:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Cliente',
            fields=[
                ('account_id', models.CharField(max_length=15, primary_key=True, serialize=False, unique=True, verbose_name='Account_id')),
                ('nome', models.CharField(max_length=128, verbose_name='Nome Completo')),
                ('email', models.EmailField(max_length=254, verbose_name='Email')),
                ('renda', models.FloatField(verbose_name='Renda Mensal')),
                ('telefone', models.CharField(max_length=14, verbose_name='Telefone')),
                ('data_nascimento', models.DateField(verbose_name='Data de Nascimento')),
                ('sexo', models.CharField(choices=[('M', 'Masculino'), ('F', 'Feminino')], max_length=32, verbose_name='Sexo')),
            ],
        ),
        migrations.CreateModel(
            name='Transacao',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False, unique=True)),
                ('data', models.DateTimeField(verbose_name='Data da Transação')),
                ('valor', models.FloatField(verbose_name='Valor')),
                ('tipo', models.CharField(max_length=128, verbose_name='Indicador Crédito / Débito')),
                ('informacoes', models.CharField(max_length=512, verbose_name='Detalhamento da Transação')),
                ('saldo_conta', models.FloatField(verbose_name='Saldo Remanescente')),
                ('cliente', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='safira.cliente', verbose_name='Cliente')),
            ],
        ),
    ]
