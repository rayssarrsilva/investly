import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models

def set_default_usuario(apps, schema_editor):
    Investimento = apps.get_model('investimentos', 'Investimento')  # Use o nome correto do app e modelo
    User = apps.get_model(settings.AUTH_USER_MODEL)  # Pega o modelo de usuário
    usuario_default = User.objects.first()  # Pegando o primeiro usuário criado

    # Atualiza todos os investimentos que não têm usuário
    Investimento.objects.filter(usuario__isnull=True).update(usuario=usuario_default)

class Migration(migrations.Migration):

    dependencies = [
        ('investimentos', '0002_remove_investimento_usuario_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='investimento',
            name='usuario',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='investimento',
            name='categoria',
            field=models.CharField(choices=[('renda_fixa', 'Renda Fixa'), ('renda_variavel', 'Renda Variável'), ('fundo_imobiliario', 'Fundo Imobiliário'), ('cripto', 'Criptomoeda')], max_length=20),
        ),
        migrations.AlterField(
            model_name='investimento',
            name='rentabilidade_anual',
            field=models.DecimalField(decimal_places=2, max_digits=5),
        ),
        migrations.AlterField(
            model_name='investimento',
            name='valor_investido',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
        # Chama a função para corrigir os dados antigos
        migrations.RunPython(set_default_usuario),
    ]
