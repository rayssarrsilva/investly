from rest_framework import serializers
from .models import Investimento

class InvestimentoSerializer(serializers.ModelSerializer):
    rentabilidade_mensal = serializers.SerializerMethodField()

    class Meta:
        model = Investimento #chama o nome da classe, modelo criado
        fields = '__all__' #inclui todos os campos
    
    @property
    def get_rentabilidade_mensal(self, obj):
        return obj.rentabilidade_mensal()
