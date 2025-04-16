from django import forms

class SimulacaoForm(forms.Form):
    valor_investido = forms.DecimalField(
        label="Valor a Investir (R$)", max_digits=10, decimal_places=2,
        widget=forms.NumberInput(attrs={
            'placeholder': 'Ex: 1000.00'
        })
    )
    percentual_cdi = forms.DecimalField(
        label="% do CDI/Selic oferecido pelo banco escolhido sobre o investimento", max_digits=5, decimal_places=2,
        widget=forms.NumberInput(attrs={
            'placeholder': 'Ex: 102'
        })
    )
    cdi_atual = forms.DecimalField(
        label="CDI ou Selic atual (% ao ano)", max_digits=5, decimal_places=2,
        widget=forms.NumberInput(attrs={
            'placeholder': 'Ex: 13.65'
        })
    )
    prazo_meses = forms.IntegerField(
        label="Prazo da aplicação (em meses)",
        widget=forms.NumberInput(attrs={
            'placeholder': 'Ex: 12'
        })
    )
    taxa_administracao = forms.DecimalField(
        label="Taxa de Administração (% ao ano)", max_digits=5, decimal_places=2,
        required=False, initial=0,
        widget=forms.NumberInput(attrs={
            'placeholder': 'Ex: 1.0'
        })
    )

class CalcularInvestimentoNecessarioForm(forms.Form):
    valor_desejado = forms.DecimalField(
        label="Objetivo Financeiro", max_digits=10, decimal_places=2,
        widget=forms.NumberInput(attrs={
            'placeholder': 'Ex: 50000.00'
        })
    )
    percentual_cdi = forms.DecimalField(
        label="% do CDI/Selic oferecido pelo investimento", max_digits=5, decimal_places=2,
        widget=forms.NumberInput(attrs={
            'placeholder': 'Ex: 102'
        })
    )
    cdi_atual = forms.DecimalField(
        label="CDI ou Selic atual (% ao ano)", max_digits=5, decimal_places=2,
        widget=forms.NumberInput(attrs={
            'placeholder': 'Ex: 13.65'
        })
    )
    valor_maximo = forms.DecimalField(
        label="Aplicação Mensal", max_digits=10, decimal_places=2,
        widget=forms.NumberInput(attrs={
            'placeholder': 'Ex: 1000.00'
        })
    )
    
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
