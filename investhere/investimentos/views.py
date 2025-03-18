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

            # Renderizar o resultado da simulação
            return render(request, 'investimentos/simulacao_resultado.html', {
                'form': form,
                'valor_futuro': valor_futuro
            })
    else:
        form = SimulacaoForm()

    # Exibir o formulário de simulação
    return render(request, 'investimentos/simulacao_form.html', {'form': form})

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
            
            return render(request, 'investimentos/calcular_resultado.html', {
                'form': form,
                'tempo_necessario': tempo_necessario,
                'valor_total': valor_total,
                'valor_desejado': valor_desejado,
                'rentabilidade_anual': rentabilidade_anual,
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

def dashboard_view(request):
    grafico1, grafico2, grafico3 = gerar_grafico()
    return render(request, 'investimentos/dashboard.html', {
        'grafico1': grafico1,
        'grafico2': grafico2,
        'grafico3': grafico3,
    })

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

def dashboard_view(request):
    return render(request, 'investimentos/dashboard_view.html')

def menu_principal(request):
    return render(request, 'investimentos/menu_principal.html')

def registro_view(request):
    return render(request, 'investimentos/registro.html')

def password_reset_request_view(request):
    if request.method == "POST":
        form = PasswordResetRequestForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            associated_users = User.objects.filter(email=email)
            if associated_users.exists():
                for user in associated_users:
                    subject = "Redefinição de Senha"
                    uid = urlsafe_base64_encode(force_bytes(user.pk))
                    token = default_token_generator.make_token(user)
                    reset_url = f"http://127.0.0.1:8000/reset/{uid}/{token}/"
                    message = f"Clique no link para redefinir sua senha: {reset_url}"
                    send_mail(subject, message, "noreply@investly.com", [email])
                messages.success(request, "Um e-mail de redefinição de senha foi enviado.")
                return redirect("login")
            else:
                messages.error(request, "Nenhuma conta encontrada com esse e-mail.")
    else:
        form = PasswordResetRequestForm()
    return render(request, "investimentos/password_reset.html", {"form": form})


def password_reset_confirm_view(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    
    if user is not None and default_token_generator.check_token(user, token):
        if request.method == "POST":
            form = PasswordResetForm(request.POST)
            if form.is_valid():
                new_password = form.cleaned_data['new_password']
                confirm_password = form.cleaned_data['confirm_password']
                if new_password == confirm_password:
                    user.set_password(new_password)
                    user.save()
                    messages.success(request, "Senha redefinida com sucesso! Faça login com sua nova senha.")
                    return redirect("login")
                else:
                    messages.error(request, "As senhas não coincidem. Tente novamente.")
        else:
            form = PasswordResetForm()
        return render(request, "investimentos/password_reset_confirm.html", {"form": form})
    else:
        messages.error(request, "O link de redefinição de senha é inválido ou expirou.")
        return redirect("password_reset")
