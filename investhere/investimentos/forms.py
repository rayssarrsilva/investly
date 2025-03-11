from django import forms

class SimulacaoForm(forms.Form):
    valor_investido = forms.DecimalField(label="Valor Investido", max_digits=10, decimal_places=2)
    rentabilidade_anual = forms.DecimalField(label="Rentabilidade Anual (%)", max_digits=5, decimal_places=2, initial=13.25)
    prazo_meses = forms.IntegerField(label="Prazo (meses)")
    taxa_administracao = forms.DecimalField(label="Taxa de Administração (%)", max_digits=5, decimal_places=2, required=False, initial=0)
    imposto_renda = forms.DecimalField(label="Imposto de Renda (%)", max_digits=5, decimal_places=2, required=False, initial=0)

class CalcularInvestimentoNecessarioForm(forms.Form):
    valor_desejado = forms.DecimalField(label="Valor Desejado", max_digits=10, decimal_places=2)
    rentabilidade_anual = forms.DecimalField(label="Rentabilidade Anual (%)", max_digits=5, decimal_places=2)
    valor_maximo = forms.DecimalField(label="Valor Máximo Disponível", max_digits=10, decimal_places=2)

class RegistroForm(forms.Form):
    username = forms.CharField(
        label="Usuário",
        max_length=150,
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Digite seu usuário"})
    )
    email = forms.EmailField(
        label="E-mail",
        widget=forms.EmailInput(attrs={"class": "form-control", "placeholder": "Digite seu e-mail"})
    )
    password = forms.CharField(
        label="Senha",
        widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Digite sua senha"})
    )

class LoginForm(forms.Form):
    username = forms.CharField(
        label="Usuário",
        max_length=150,
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Digite seu usuário"})
    )
    password = forms.CharField(
        label="Senha",
        widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Digite sua senha"})
    )

class PasswordResetRequestForm(forms.Form):
    email = forms.EmailField(
        label="E-mail",
        widget=forms.EmailInput(attrs={"class": "form-control", "placeholder": "Digite seu e-mail para redefinir a senha"})
    )

class PasswordResetForm(forms.Form):
    new_password = forms.CharField(
        label="Nova Senha",
        widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Digite a nova senha"})
    )
    confirm_password = forms.CharField(
        label="Confirme a Senha",
        widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Confirme a nova senha"})
    )
