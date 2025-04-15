from rest_framework import serializers
from .models import *

class CadernetaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Caderneta
        fields = '__all__'

class PacoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pacote
        fields = ('id','titulo', 'descricao', 'preco', 'qnt_cromos', 'imagem')


