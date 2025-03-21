# Generated by Django 5.1.6 on 2025-03-16 22:39

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('investimentos', '0005_auto_20250222_1358'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='SimulacaoHistorico',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipo_simulacao', models.CharField(max_length=50)),
                ('valor_inicial', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('rentabilidade_anual', models.DecimalField(decimal_places=2, max_digits=5)),
                ('prazo_meses', models.IntegerField(blank=True, null=True)),
                ('taxa_administracao', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
                ('imposto_renda', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
                ('valor_futuro', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('valor_desejado', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('valor_maximo', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('tempo_necessario', models.IntegerField(blank=True, null=True)),
                ('valor_total', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('data_criacao', models.DateTimeField(auto_now_add=True)),
                ('usuario', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
