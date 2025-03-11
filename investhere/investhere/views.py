# investhere/viewos.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class LogoutView(APIView):
    def post(self, request):
        # A única ação necessária é remover o token do lado do cliente
        return Response({"message": "Logout realizado com sucesso!"}, status=status.HTTP_200_OK)
