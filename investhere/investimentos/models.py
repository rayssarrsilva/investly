from django.db import models  
from django.contrib.auth.models import User  

class Investimento(models.Model):
    CATEGORIAS = [
        ('renda_fixa', 'Renda Fixa'),
        ('renda_variavel', 'Renda Variável'),
        ('fundo_imobiliario', 'Fundo Imobiliário'),
        ('cripto', 'Criptomoeda'),
    ]

    usuario = models.ForeignKey(User, on_delete=models.CASCADE)  
    nome = models.CharField(max_length=255)  
    categoria = models.CharField(max_length=20, choices=CATEGORIAS) 
    valor_investido = models.DecimalField(max_digits=10, decimal_places=2)  
    rentabilidade_anual = models.DecimalField(max_digits=5, decimal_places=2)  
    data_aplicacao = models.DateField()  
    prazo_meses = models.IntegerField() 

    def rentabilidade_mensal(self):
        """Calcula a rentabilidade mensal com base na anual."""
        return round(float(self.rentabilidade_anual) / 12, 2)

    def __str__(self):
        return f"{self.nome} - {self.usuario.username if self.usuario else 'Sem usuário'}"
    
class SimulacaoHistorico(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    tipo_simulacao = models.CharField(max_length=50)  # "Investimento" ou "Necessário"
    valor_inicial = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    rentabilidade_anual = models.DecimalField(max_digits=5, decimal_places=2)
    prazo_meses = models.IntegerField(null=True, blank=True)
    taxa_administracao = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    imposto_renda = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    valor_futuro = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    valor_desejado = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    valor_maximo = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    tempo_necessario = models.IntegerField(null=True, blank=True)
    valor_total = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    data_criacao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Simulação de {self.usuario} - {self.tipo_simulacao}"
