from django.urls import path
from investhere.views import LogoutView
from .views import (
    InvestimentoViewSet,
    simulacao_investimento_view,
    calcular_investimento_necessario_view,
    login_view,
    menu_principal,
    historico_simulacoes_view,
    excluir_todas_simulacoes,
    excluir_simulacao,)

urlpatterns = [
    path('investimentos/', InvestimentoViewSet.as_view({'get': 'list'}), name='investimentos-list'),
    path('simulacao/', simulacao_investimento_view, name='simulacao-investimentos'),
    path('calcular-investimento-necessario/', calcular_investimento_necessario_view, name='calcular-investimento-necessario'),
    path('login/', login_view, name='login'),
    path('', login_view, name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('menu_principal/', menu_principal, name='menu_principal'),
    path('historico/', historico_simulacoes_view, name='historico_simulacoes'),
    path('historico/excluir/<int:simulacao_id>/', excluir_simulacao, name='excluir_simulacao'),
    path('historico/excluir-todas/', excluir_todas_simulacoes, name='excluir_todas_simulacoes'),
]
