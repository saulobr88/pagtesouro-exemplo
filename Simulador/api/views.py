from django.contrib.auth.models import User, Group
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import (viewsets, permissions)
from rest_framework.status import (
    HTTP_200_OK, HTTP_201_CREATED, HTTP_400_BAD_REQUEST
)
from .serializers import (
    UserSerializer, 
    GroupSerializer,
    GruPagamentoSerializer,
)
import uuid, string, random
from datetime import datetime

def gerar_string_alfanumerica(tamanho):
    caracteres = string.ascii_letters + string.digits  # Letras maiúsculas, minúsculas e números
    string_gerada = ''.join(random.choice(caracteres) for _ in range(tamanho))
    return string_gerada

class HomeApiView(APIView):
    def get(self, request, format=None):
        return Response({"nome":"PagTesouro Simulador API", "version":"1.0"}, status=200)

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]

class GruPagamentoAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request, format=None):
        serializer = GruPagamentoSerializer(data=request.data)

        # Simule a criação de um ID único
        id_pagamento = gerar_string_alfanumerica(22)
        id_sessao = str(uuid.uuid4())

        # Simule a data de criação como a data atual
        data_criacao = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")

        # Construa a resposta desejada
        response_data = {
            "idPagamento": id_pagamento,
            "dataCriacao": data_criacao,
            "proximaUrl": f"https://valpagtesouro.tesouro.gov.br/#/pagamento?idSessao={id_sessao}",
            "situacao": {
                "codigo": "CRIADO"
            }
        }

        # return Response(serializer.initial_data, status=HTTP_200_OK)
        return Response(response_data, status=HTTP_200_OK)
    
class GruPagamentoNotificacaoAPIView(APIView):
    def post(self, request, format=None):
        # Verifica se o corpo da requisição está no formato esperado
        expected_keys = [
            "idPagamento",
            "dataHora",
        ]

        for key in expected_keys:
            if key not in request.data:
                return Response(
                    {"mensagem": f"{key} não encontrado no corpo da requisição."},
                    status=HTTP_400_BAD_REQUEST,
                )

        # Construa a resposta desejada
        response_data = {
            "idPagamento": request.data.get('idPagamento'),
            "dataHora": request.data.get('dataHora'),
            "status": HTTP_200_OK
        }

        # return Response(serializer.initial_data, status=HTTP_200_OK)
        return Response(response_data, status=HTTP_200_OK)
    
class GruPagamentoConsultaAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, id_pagamento, format=None):
        data_criacao = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")

        # Construa a resposta desejada
        response_data = {
            "idPagamento": str(id_pagamento),
            "tipoPagamentoEscolhido": "CARTAO_CREDITO",
            "valor": 100,
            "nomePSP": "Simulador PSP",
            "transacaoPSP": "3djVYxnwfSIOUY61S0SsF",
            "situacao": {
                "codigo": "CONCLUIDO",
                "data": data_criacao
            }
        }
        # return Response(serializer.initial_data, status=HTTP_200_OK)
        return Response(response_data, status=HTTP_200_OK)