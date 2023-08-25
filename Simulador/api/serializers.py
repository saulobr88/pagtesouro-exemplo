from django.contrib.auth.models import User, Group
from rest_framework import serializers


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']

class GruPagamentoSerializer(serializers.Serializer):
    codigoServico = serializers.CharField(max_length=255)
    referencia = serializers.CharField(max_length=255)
    competencia = serializers.CharField(max_length=255)
    vencimento = serializers.CharField(max_length=255)
    cnpjCpf = serializers.CharField(max_length=255)
    nomeContribuinte = serializers.CharField(max_length=255)
    valorPrincipal = serializers.CharField(max_length=255)
    valorDescontos = serializers.CharField(max_length=255)
    valorOutrasDeducoes = serializers.CharField(max_length=255)
    valorMulta = serializers.CharField(max_length=255)
    valorJuros = serializers.CharField(max_length=255)
    valorOutrosAcrescimos = serializers.CharField(max_length=255)
    modoNavegacao = serializers.CharField(max_length=255)
    urlNotificacao = serializers.CharField(max_length=255)
