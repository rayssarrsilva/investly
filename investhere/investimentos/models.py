from django.db import models  # type: ignore
from django.contrib.auth.models import User  # type: ignore

class Investimento(models.Model):
    CATEGORIAS = [
        ('renda_fixa', 'Renda Fixa'),
        ('renda_variavel', 'Renda Variável'),
        ('fundo_imobiliario', 'Fundo Imobiliário'),
        ('cripto', 'Criptomoeda'),
    ]

    usuario = models.ForeignKey(User, on_delete=models.CASCADE)  # Agora obrigatório!
    nome = models.CharField(max_length=255)  # Nome do investimento
    categoria = models.CharField(max_length=20, choices=CATEGORIAS)  # Tipo do investimento
    valor_investido = models.DecimalField(max_digits=10, decimal_places=2)  # armazena o valor aplicado no investimento
    rentabilidade_anual = models.DecimalField(max_digits=5, decimal_places=2)  # armazena a rentabilidade anual percentual do investimento.
    data_aplicacao = models.DateField()  # Data em que foi feito o investimento
    prazo_meses = models.IntegerField()  # Prazo que o investimento terá em meses

    def rentabilidade_mensal(self):
        """Calcula a rentabilidade mensal com base na anual."""
        return round(float(self.rentabilidade_anual) / 12, 2)

    def __str__(self):
        return f"{self.nome} - {self.usuario.username if self.usuario else 'Sem usuário'}"