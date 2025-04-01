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

# Classe InvestimentoViewSet
class InvestimentoViewSet(viewsets.ModelViewSet):
    queryset = Investimento.objects.all()
    serializer_class = InvestimentoSerializer
    permission_classes = [IsAuthenticated]

# Função de cálculo da rentabilidade mensal
def calcular_rentabilidade_mensal(rentabilidade_anual, taxa_administracao=0, imposto_renda=0):
    rentabilidade_liquida = rentabilidade_anual - (rentabilidade_anual * taxa_administracao) - (rentabilidade_anual * imposto_renda)
    return rentabilidade_liquida / 12

# Função de cálculo do valor futuro
def calcular_valor_futuro(valor_investido, rentabilidade_anual, prazo_meses, aporte_mensal=0, taxa_administracao=0, imposto_renda=0):
    rentabilidade_mensal = calcular_rentabilidade_mensal(rentabilidade_anual, taxa_administracao, imposto_renda)
    valor_futuro = valor_investido

    for _ in range(prazo_meses):
        valor_futuro += valor_futuro * (rentabilidade_mensal / 100)
        valor_futuro += aporte_mensal
    
    return round(valor_futuro, 2)

# View para Simulação de Investimento
from .models import SimulacaoHistorico

def simulacao_investimento_view(request):
    if request.method == "POST":
        form = SimulacaoForm(request.POST)
        if form.is_valid():
            valor_investido = form.cleaned_data['valor_investido']
            rentabilidade_anual = form.cleaned_data['rentabilidade_anual']
            prazo_meses = form.cleaned_data['prazo_meses']
            taxa_administracao = form.cleaned_data['taxa_administracao']
            imposto_renda = form.cleaned_data['imposto_renda']

            # Calcular o valor futuro do investimento
            valor_futuro = calcular_valor_futuro(valor_investido, rentabilidade_anual, prazo_meses, 0, taxa_administracao, imposto_renda)

            # Salvar no histórico
            SimulacaoHistorico.objects.create(
                usuario=request.user if request.user.is_authenticated else None,
                tipo_simulacao="Investimento",
                valor_inicial=valor_investido,
                rentabilidade_anual=rentabilidade_anual,
                prazo_meses=prazo_meses,
                taxa_administracao=taxa_administracao,
                imposto_renda=imposto_renda,
                valor_futuro=valor_futuro,
            )

            # Renderizar o resultado da simulação
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
    if request.method == "POST":
        form = CalcularInvestimentoNecessarioForm(request.POST)
        if form.is_valid():
            valor_desejado = form.cleaned_data['valor_desejado']
            rentabilidade_anual = form.cleaned_data['rentabilidade_anual']
            valor_maximo = form.cleaned_data['valor_maximo']

            # Calcular o tempo necessário
            tempo_necessario = calcular_tempo_necessario(valor_desejado, rentabilidade_anual, valor_maximo)

            # Calcular o valor total acumulado até lá
            valor_total = calcular_valor_futuro(0, rentabilidade_anual, tempo_necessario, valor_maximo)

            # Salvar no histórico como "Investimento Necessário"
            SimulacaoHistorico.objects.create(
                usuario=request.user if request.user.is_authenticated else None,
                tipo_simulacao="Investimento Necessário",
                valor_inicial=0,  # Indica que o investimento foi planejado a partir de aportes
                rentabilidade_anual=rentabilidade_anual,
                valor_desejado=valor_desejado,
                valor_maximo=valor_maximo,
                tempo_necessario=tempo_necessario,
                valor_futuro=valor_total,  # Usando o valor total como resultado da simulação
                data_criacao=timezone.now()
            )

            return render(request, 'investimentos/calcular_resultado.html', {
                'form': form,
                'tempo_necessario': tempo_necessario,
                'valor_total': valor_total,
                'valor_desejado': valor_desejado,
                'valor_maximo': valor_maximo,
            })
    else:
        form = CalcularInvestimentoNecessarioForm()
    return render(request, 'investimentos/calcular_form.html', {'form': form})
# Função de cálculo do tempo necessário para atingir o valor desejado usado na função calcular_investimento_necessario_view (Formulario)
def calcular_tempo_necessario(valor_desejado, rentabilidade_anual, valor_maximo):
    if valor_maximo <= 0:
        return "Valor máximo deve ser maior que zero."
    rentabilidade_mensal = rentabilidade_anual / 12 / 100  
    try:
        meses_necessarios = math.log((valor_desejado * rentabilidade_mensal / valor_maximo) + 1) / math.log(1 + rentabilidade_mensal)
        meses_necessarios = math.ceil(meses_necessarios)  
    except ValueError:
        raise ValueError("Parâmetros inválidos para cálculo!")
    
    return meses_necessarios


#Função para renderizar o template com as explicações dos cálculos
def explicacao_calculo_view(request):
    return render(request, 'investimentos/explicacao.html')

def gerar_grafico():
    investimentos = Investimento.objects.all()
    nomes = [inv.nome for inv in investimentos]
    valores_iniciais = [inv.valor_inicial for inv in investimentos]
    valores_futuros = [inv.valor_futuro for inv in investimentos]
    rentabilidades = [inv.rentabilidade_anual / 12 for inv in investimentos]
    prazos = [inv.prazo_meses for inv in investimentos]

    # 1️⃣ Gráfico de Rentabilidade Mensal
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.bar(nomes, rentabilidades, color='blue')
    ax.set_xlabel("Investimentos")
    ax.set_ylabel("Rentabilidade Mensal (%)")
    ax.set_title("Rentabilidade Mensal dos Investimentos")
    img1 = io.BytesIO()
    plt.savefig(img1, format='png')
    img1.seek(0)
    grafico1 = base64.b64encode(img1.getvalue()).decode()
    plt.close()

    # 2️⃣ Comparação: Valor Inicial x Valor Futuro
    fig, ax = plt.subplots(figsize=(6, 4))
    x = np.arange(len(nomes))
    width = 0.35
    ax.bar(x - width/2, valores_iniciais, width, label='Valor Inicial', color='gray')
    ax.bar(x + width/2, valores_futuros, width, label='Valor Futuro', color='green')
    ax.set_xticks(x)
    ax.set_xticklabels(nomes, rotation=45)
    ax.set_xlabel("Investimentos")
    ax.set_ylabel("Valor (R$)")
    ax.set_title("Comparação: Valor Investido vs Valor Futuro")
    ax.legend()
    img2 = io.BytesIO()
    plt.savefig(img2, format='png')
    img2.seek(0)
    grafico2 = base64.b64encode(img2.getvalue()).decode()
    plt.close()

    # 3️⃣ Gráfico de Tempo Necessário para Alcançar o Valor Desejado
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.plot(valores_futuros, prazos, marker='o', linestyle='-', color='red')
    ax.set_xlabel("Valor Futuro (R$)")
    ax.set_ylabel("Meses Necessários")
    ax.set_title("Tempo Necessário para Atingir o Valor Desejado")
    img3 = io.BytesIO()
    plt.savefig(img3, format='png')
    img3.seek(0)
    grafico3 = base64.b64encode(img3.getvalue()).decode()
    plt.close()

    return grafico1, grafico2, grafico3



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

def registro_view(request):
    return render(request, 'investimentos/registro.html')