# Generated by Django 5.1.1 on 2025-02-12 17:19

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Investimento',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=255)),
                ('categoria', models.CharField(choices=[('renda_fixa', 'Renda Fixa'), ('renda_variavel', 'Renda Variável'), ('fundo_imobiliario', 'Fundo Imobiliário'), ('cripto', 'Criptomoeda')], max_length=20)),
                ('valor_investido', models.DecimalField(decimal_places=2, max_digits=10)),
                ('rentabilidade_anual', models.DecimalField(decimal_places=2, max_digits=5)),
                ('data_aplicacao', models.DateField()),
                ('prazo_meses', models.IntegerField()),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
