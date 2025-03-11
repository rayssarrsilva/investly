from django.test import TestCase

# Teste de Criação e Listagem de Investimentos
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from .models import Investimento
from rest_framework_simplejwt.tokens import RefreshToken
import uuid


class InvestimentoTests(APITestCase):
    
    def setUp(self):
        # Cria um usuário com nome único para evitar conflito
        username = f'testuser_{uuid.uuid4()}'
        self.user = User.objects.create_user(username=username, password='testpassword')
        
        # Cria um token de acesso para esse usuário
        refresh = RefreshToken.for_user(self.user)
        self.access_token = str(refresh.access_token)
        
        # Configura o cabeçalho com o token de acesso
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)

    def test_create_investimento(self):
        # Dados para criar um investimento
        data = {
            'nome': 'Investimento Teste',
            'categoria': 'renda_fixa',
            'valor_investido': '1000.00',
            'rentabilidade_anual': '5.00',
            'data_aplicacao': '2025-02-22',
            'prazo_meses': 12,
            'usuario': self.user.id  # Passa o ID do usuário criado no setUp
        }

        # Faz a requisição POST
        response = self.client.post('/api/investimentos/', data, format='json')

        # Verifica se o status da resposta é 201 CREATED
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_list_investimentos(self):
        # Testa a listagem de investimentos
        response = self.client.get('/api/investimentos/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
