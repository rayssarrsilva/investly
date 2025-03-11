from django.urls import path
from investhere.views import LogoutView
from .views import (
    InvestimentoViewSet,
    simulacao_investimento_view,
    calcular_investimento_necessario_view,
    login_view,
    dashboard_view,
    explicacao_calculo_view,
    menu_principal,
    registro_view)

urlpatterns = [
    # Registrando as URLs com o DefaultRouter para o InvestimentoViewSet
    path('investimentos/', InvestimentoViewSet.as_view({'get': 'list'}), name='investimentos-list'),
    
    # URL para simulação de investimentos (formulário)
    path('simulacao/', simulacao_investimento_view, name='simulacao-investimentos'),

    # URL para calcular o valor necessário para atingir um objetivo financeiro (formulário)
    path('calcular-investimento-necessario/', calcular_investimento_necessario_view, name='calcular-investimento-necessario'),

    # URL de login
    path('login/', login_view, name='login'),

    path('registro/', registro_view, name='registro'),

    #Dashboard
    path('dashboard/', dashboard_view, name='dashboard'),

    # URL de logout (possivelmente para uma operação POST)
    path('logout/', LogoutView.as_view(), name='logout'),

    path('calculo-explicacao/', explicacao_calculo_view, name='calculo_explicacao'),
    
    path('menu_principal/', menu_principal, name='menu_principal')
]
