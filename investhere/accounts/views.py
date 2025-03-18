from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib import messages
from .forms import RegisterForm
from django.contrib.auth.models import User


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            email = form.cleaned_data["email"]

            # Verifica se o nome de usuário ou e-mail já existem
            if User.objects.filter(username=username).exists():
                messages.error(request, "Esse nome de usuário já está em uso. Escolha outro.")
            elif User.objects.filter(email=email).exists():
                messages.error(request, "Este e-mail já está cadastrado. Use outro ou faça login.")
            else:
                user = form.save(commit=False)
                user.set_password(form.cleaned_data["password1"])  # Criptografa a senha corretamente
                user.save()
                login(request, user)
                messages.success(request, 'Registro bem-sucedido!')
                return redirect('dashboard')
        else:
            messages.error(request, "Erro no formulário. Verifique os campos preenchidos.")

    else:
        form = RegisterForm()

    return render(request, 'investimentos/registro.html', {'form': form})



def user_logout(request):
    logout(request)
    messages.info(request, 'Você saiu da conta.')
    return redirect('login')

def dashboard(request):
    return render(request, 'investimentos/dashboard_view.html')
