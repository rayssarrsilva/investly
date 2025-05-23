import math
from django.shortcuts import render
from rest_framework import viewsets
from .models import Investimento
from .serializers import InvestimentoSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from django.contrib.auth.decorators import login_required
from .forms import SimulacaoForm, CalcularInvestimentoNecessarioForm
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, get_user_model
from django.contrib import messages
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils import timezone
from django.utils.encoding import force_bytes, force_str
from .forms import RegistroForm, LoginForm, PasswordResetRequestForm, PasswordResetForm
import matplotlib.pyplot as plt
import numpy as np
import io
import base64
from decimal import Decimal


class InvestimentoViewSet(viewsets.ModelViewSet):
    queryset = Investimento.objects.all()
    serializer_class = InvestimentoSerializer
    permission_classes = [IsAuthenticated]

def calcular_rentabilidade_mensal(percentual_cdi, cdi_atual, taxa_administracao=0, imposto_renda=0):
    # Converte tudo para float para evitar erro com Decimal
    percentual_cdi = float(percentual_cdi)
    cdi_atual = float(cdi_atual)
    taxa_administracao = float(taxa_administracao)
    imposto_renda = float(imposto_renda)

    # Calcula CDI mensal a partir do anual
    cdi_mensal = (1 + (cdi_atual / 100)) ** (1 / 12) - 1

    # Calcula a rentabilidade líquida
    rentabilidade_bruta = cdi_mensal * (percentual_cdi / 100)
    rentabilidade_liquida = rentabilidade_bruta * (1 - taxa_administracao / 100) * (1 - imposto_renda / 100)

    return rentabilidade_liquida


def calcular_valor_futuro(valor_investido, percentual_cdi, cdi_atual, prazo_meses, aporte_mensal=0, taxa_administracao=0, imposto_renda=0):
    # Converte os valores para float para evitar conflitos com Decimal
    valor_futuro = float(valor_investido)
    aporte_mensal = float(aporte_mensal)

    rentabilidade_mensal = calcular_rentabilidade_mensal(percentual_cdi, cdi_atual, taxa_administracao, imposto_renda)

    for _ in range(prazo_meses):
        valor_futuro += valor_futuro * rentabilidade_mensal
        valor_futuro += aporte_mensal

    return round(valor_futuro, 2)


# View para Simulação de Investimento PRINCIPAL
from django.shortcuts import render
from .models import SimulacaoHistorico

def simulacao_investimento_view(request):
    if request.method == "POST":
        form = SimulacaoForm(request.POST)
        if form.is_valid():
            valor_investido = form.cleaned_data['valor_investido']
            percentual_cdi = form.cleaned_data['percentual_cdi']
            cdi_atual = form.cleaned_data['cdi_atual']
            prazo_meses = form.cleaned_data['prazo_meses']
            taxa_administracao = form.cleaned_data['taxa_administracao'] or 0
            imposto_renda = form.cleaned_data.get('imposto_renda', 0) or 0

            valor_futuro = calcular_valor_futuro(valor_investido, percentual_cdi, cdi_atual, prazo_meses, 0, taxa_administracao, imposto_renda)

            SimulacaoHistorico.objects.create(
                usuario=request.user if request.user.is_authenticated else None,
                tipo_simulacao="Investimento",
                valor_inicial=valor_investido,
                rentabilidade_anual=percentual_cdi,  # Armazenando % do CDI
                prazo_meses=prazo_meses,
                taxa_administracao=taxa_administracao,
                valor_futuro=valor_futuro,
            )

            return render(request, 'investimentos/simulacao_resultado.html', {
                'form': form,
                'valor_futuro': valor_futuro
            })
    else:
        form = SimulacaoForm()
    return render(request, 'investimentos/simulacao_form.html', {'form': form})

#HISTORICO DE SIMULAÇÕES --------------------------------------------
def historico_simulacoes_view(request):
    historico = SimulacaoHistorico.objects.filter(usuario=request.user).order_by('-data_criacao') if request.user.is_authenticated else []
    return render(request, 'investimentos/historico.html', {'historico': historico})

def excluir_simulacao(request, simulacao_id):
    simulacao = SimulacaoHistorico.objects.filter(id=simulacao_id, usuario=request.user).first()
    if simulacao:
        simulacao.delete()
        messages.success(request, "Simulação excluída com sucesso.")
    return redirect('historico_simulacoes')

def excluir_todas_simulacoes(request):
    if request.user.is_authenticated:
        SimulacaoHistorico.objects.filter(usuario=request.user).delete()
        messages.success(request, "Todo o histórico foi excluído com sucesso.")
    return redirect('historico_simulacoes')

def historico_simulacoes_template(request):
    historico = SimulacaoHistorico.objects.filter(usuario=request.user).order_by('-data_criacao') if request.user.is_authenticated else []
    return render(request, 'investimentos/historico.html', {
        'historico': historico,
        'excluir_todas_url': 'excluir_todas_simulacoes',
        'excluir_simulacao_url': 'excluir_simulacao'
    })

def historico_simulacoes_view(request):
    if request.user.is_authenticated:
        historico = SimulacaoHistorico.objects.filter(usuario=request.user).order_by('-data_criacao')
    else:
        historico = []

    return render(request, 'investimentos/historico.html', {'historico': historico})

#-----------------------------------------------------------
# View para Calcular Investimento Necessário
def calcular_investimento_necessario_view(request):
    form = CalcularInvestimentoNecessarioForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        cd = form.cleaned_data
        valor_desejado = cd.get('valor_desejado', 0) or 0
        percentual_cdi = cd.get('percentual_cdi', 0) or 0
        cdi_atual = cd.get('cdi_atual', 0) or 0
        valor_maximo = cd.get('valor_maximo', 0) or 0

        try:
            rentabilidade_anual = (percentual_cdi / 100) * cdi_atual
            tempo_necessario = calcular_tempo_necessario(valor_desejado, rentabilidade_anual, valor_maximo)
            valor_total = calcular_valor_futuro(0, percentual_cdi, cdi_atual, tempo_necessario, valor_maximo)
        except ValueError as e:
            messages.error(request, str(e))
            return render(request, 'investimentos/calcular_form.html', {'form': form})

        SimulacaoHistorico.objects.create(
            usuario=request.user if request.user.is_authenticated else None,
            tipo_simulacao="Investimento Necessário",
            valor_inicial=0,
            rentabilidade_anual=percentual_cdi,
            valor_desejado=valor_desejado,
            valor_maximo=valor_maximo,
            tempo_necessario=tempo_necessario,
            valor_futuro=valor_total,
            data_criacao=timezone.now()
        )
        return render(request, 'investimentos/calcular_resultado.html', {
            'tempo_necessario': tempo_necessario,
            'valor_total': valor_total,
            'valor_desejado': valor_desejado,
            'valor_maximo': valor_maximo
        })
    return render(request, 'investimentos/calcular_form.html', {'form': form})

# Função de cálculo do tempo necessário para atingir o valor desejado usado na função calcular_investimento_necessario_view (Formulario)
def calcular_tempo_necessario(valor_desejado, rentabilidade_anual, valor_maximo):
    valor_desejado = float(valor_desejado)
    rentabilidade_anual = float(rentabilidade_anual)
    valor_maximo = float(valor_maximo)

    if valor_maximo <= 0:
        raise ValueError("O valor máximo deve ser maior que zero.")

    rentabilidade_mensal = rentabilidade_anual / 12 / 100

    if rentabilidade_mensal == 0:
        raise ValueError("A rentabilidade mensal não pode ser zero.")

    try:
        meses_necessarios = math.log((valor_desejado * rentabilidade_mensal / valor_maximo) + 1) / math.log(1 + rentabilidade_mensal)
        return math.ceil(meses_necessarios)
    except ValueError:
        raise ValueError("Parâmetros inválidos para cálculo!")


# Classe para Logout
class LogoutView(APIView):
    def post(self, request):
        return Response({"message": "Logout realizado com sucesso!"}, status=status.HTTP_200_OK)

#função para acessar o arquivo login.html
def login_view(request):
    form = LoginForm(request.POST or None)
    
    if request.method == "POST":
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect("menu_principal")
            else:
                messages.error(request, "Usuário ou senha inválidos.")

    return render(request, "investimentos/login.html", {"form": form})

def menu_principal(request):
    return render(request, 'investimentos/menu_principal.html')