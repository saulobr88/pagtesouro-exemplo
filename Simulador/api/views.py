from django.contrib.auth.models import User, Group
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import (viewsets, permissions)
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_500_INTERNAL_SERVER_ERROR
)
from .serializers import (
    UserSerializer, 
    GroupSerializer,
    GruPagamentoSerializer,
)
import uuid, string, random
from datetime import datetime
from api.models import Pagamento

def gerar_string_alfanumerica(tamanho):
    caracteres = string.ascii_letters + string.digits  # Letras maiúsculas, minúsculas e números
    string_gerada = ''.join(random.choice(caracteres) for _ in range(tamanho))
    return string_gerada

class HomeApiView(APIView):
    def get(self, request, format=None):
        return Response({"nome":"PagTesouro Simulador API", "version":"1.0"}, status=HTTP_200_OK)

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

        pagamento = Pagamento()
        request_status = HTTP_201_CREATED

        if (serializer.is_valid()):    
            pagamento.idPagamento = id_pagamento
            pagamento.idSessao = id_sessao
            pagamento.dataCriacao = data_criacao
            pagamento.codigoServico = serializer.validated_data.get('codigoServico')
            pagamento.referencia = serializer.validated_data.get('referencia')
            pagamento.competencia = serializer.validated_data.get('competencia')
            pagamento.vencimento = serializer.validated_data.get('vencimento')
            pagamento.cnpjCpf = serializer.validated_data.get('cnpjCpf')
            pagamento.nomeContribuinte = serializer.validated_data.get('nomeContribuinte')
            pagamento.valorPrincipal = serializer.validated_data.get('valorPrincipal')
            pagamento.valorDescontos = serializer.validated_data.get('valorDescontos')
            pagamento.valorOutrasDeducoes = serializer.validated_data.get('valorOutrasDeducoes')
            pagamento.valorMulta = serializer.validated_data.get('valorMulta')
            pagamento.valorJuros = serializer.validated_data.get('valorJuros')
            pagamento.valorOutrosAcrescimos = serializer.validated_data.get('valorOutrosAcrescimos')
            pagamento.modoNavegacao = serializer.validated_data.get('modoNavegacao')
            pagamento.urlNotificacao = serializer.validated_data.get('urlNotificacao')
            pagamento.proximaUrl = str("https://valpagtesouro.tesouro.gov.br/#/pagamento?idSessao=" + id_sessao)
            pagamento.tipoPagamentoEscolhido = ""
            pagamento.nomePSP = ""
            pagamento.transacaoPSP = ""
            pagamento.situacao_codigo = "CRIADO"
            pagamento.situacao_dataHora = data_criacao

            pagamento.save()

        if (pagamento.id):
            # Construa a resposta desejada
            response_data = {
                "idPagamento": id_pagamento,
                "dataCriacao": data_criacao,
                "proximaUrl": f"https://valpagtesouro.tesouro.gov.br/#/pagamento?idSessao={id_sessao}",
                "situacao": {
                    "codigo": "CRIADO"
                }
            }
        else:
            response_data = {
                "idPagamento": id_pagamento,
                "dataCriacao": data_criacao,
                "proximaUrl": f"https://valpagtesouro.tesouro.gov.br/#/pagamento?idSessao={id_sessao}",
                "situacao": {
                    "codigo": "ERRO"
                }
            }
            request_status = HTTP_500_INTERNAL_SERVER_ERROR

        # return Response(serializer.initial_data, status=HTTP_200_OK)
        return Response(response_data, status=request_status)
    
class GruPagamentoNotificacaoAPIView(APIView):
    def post(self, request, format=None):
        # Verifica se o corpo da requisição está no formato esperado
        expected_keys = [
            "idPagamento",
            "dataHora",
            "situacaoCodigo"
        ]

        for key in expected_keys:
            if key not in request.data:
                return Response(
                    {"mensagem": f"{key} não encontrado no corpo da requisição."},
                    status=HTTP_400_BAD_REQUEST,
                )

        request_status = HTTP_200_OK
        pagamento = Pagamento.objects.get(idPagamento=str(request.data.get('idPagamento')))
        if (pagamento.id):
            pagamento.situacao_codigo = request.data.get('situacaoCodigo')
            pagamento.situacao_dataHora = request.data.get('dataHora')
            pagamento.save()

            # Construa a resposta desejada
            response_data = {
                "idPagamento": pagamento.idPagamento,
                "situacao": {
                    "codigo": pagamento.situacao_codigo,
                    "data": pagamento.situacao_dataHora
                }
            }
        else:
            request_status = HTTP_404_NOT_FOUND
            response_data = {
                "idPagamento": request.data.get('idPagamento'),
                "situacao": {
                    "codigo": 'NOT FOUND',
                    "data": 'NOT FOUND'
                }
            }

        return Response(response_data, status=request_status)

class GruPagamentoConsultaAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, id_pagamento, format=None):
        request_status = HTTP_200_OK

        pagamento = Pagamento.objects.get(idPagamento=str(id_pagamento))
        if (pagamento.id):
            # Construa a resposta desejada
            response_data = {
                "idPagamento": pagamento.idPagamento,
                "tipoPagamentoEscolhido": pagamento.tipoPagamentoEscolhido,
                "valor": pagamento.valorPrincipal,
                "nomePSP": pagamento.nomePSP,
                "transacaoPSP": pagamento.transacaoPSP,
                "situacao": {
                    "codigo": pagamento.situacao_codigo,
                    "data": pagamento.situacao_dataHora
                }
            }
        else:
            response_data = {
                "idPagamento": id_pagamento,
                "tipoPagamentoEscolhido": 'NOT FOUND',
                "valor": 'NOT FOUND',
                "nomePSP": 'NOT FOUND',
                "transacaoPSP": 'NOT FOUND',
                "situacao": {
                    "codigo": 'NOT FOUND',
                    "data": 'NOT FOUND'
                }
            }
            request_status = HTTP_404_NOT_FOUND

        return Response(response_data, status=request_status)
