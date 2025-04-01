from django.urls import path
from investhere.views import LogoutView
from .views import (
    InvestimentoViewSet,
    simulacao_investimento_view,
    calcular_investimento_necessario_view,
    login_view,
    explicacao_calculo_view,
    menu_principal,
    historico_simulacoes_view,
    excluir_todas_simulacoes,
    excluir_simulacao,)

urlpatterns = [
    # Registrando as URLs com o DefaultRouter para o InvestimentoViewSet
    path('investimentos/', InvestimentoViewSet.as_view({'get': 'list'}), name='investimentos-list'),
    
    # URL para simulação de investimentos (formulário)
    path('simulacao/', simulacao_investimento_view, name='simulacao-investimentos'),

    # URL para calcular o valor necessário para atingir um objetivo financeiro (formulário)
    path('calcular-investimento-necessario/', calcular_investimento_necessario_view, name='calcular-investimento-necessario'),

    # URL de login
    path('login/', login_view, name='login'),
    
    path('', login_view, name='login'),

    # URL de logout (possivelmente para uma operação POST)
    path('logout/', LogoutView.as_view(), name='logout'),

    path('calculo-explicacao/', explicacao_calculo_view, name='calculo_explicacao'),
    
    path('menu_principal/', menu_principal, name='menu_principal'),

    path('historico/', historico_simulacoes_view, name='historico_simulacoes'),

    path('historico/excluir/<int:simulacao_id>/', excluir_simulacao, name='excluir_simulacao'),

    path('historico/excluir-todas/', excluir_todas_simulacoes, name='excluir_todas_simulacoes'),

]
