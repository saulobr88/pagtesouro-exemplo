from http import HTTPStatus
from datetime import datetime, date
import requests
from django.conf import settings
from .helper_service import HelperService

class PagTesouroService:
    def __init__(self):
        self.token = settings.PAGTESOURO_CLIENT["JWT_TOKEN_ACCESS"]
        self.base_url = settings.PAGTESOURO_CLIENT["API_BASE_URL"]

    def getBaseUrl(self):
        return self.base_url.rstrip('/')

    def getHeaders(self):
        return {
            'Authorization': f'Bearer {self.token}'
        }

    def getSanitizedData(self, request):
        helperService = HelperService()
        valorPrincipal = 0.0
        taxaId = request.POST['valorPrincipal']

        if (taxaId):
            taxas = helperService.getVestibularTaxas()
            for taxa in taxas:
                if (taxaId == str(taxa.id)):
                    valorPrincipal = taxa.valor

        hoje = date.today()
        vencimento = date.today().replace(year = date.today().year + 1)

        return {
            "codigoServico": "203",
            "referencia": "321",
            "competencia": str(datetime.strftime(hoje, '%m%Y')),
            "vencimento": str(datetime.strftime(vencimento, '%d%m%Y')),
            "cnpjCpf": str(request.POST['cnpjCpf']),
            "nomeContribuinte": str(request.POST['nomeContribuinte']),
            "valorPrincipal": valorPrincipal,
            "valorDescontos": "0",
            "valorOutrasDeducoes": "0",
            "valorMulta": "0",
            "valorJuros": "0",
            "valorOutrosAcrescimos": "0",
            "modoNavegacao": "2",
            "urlNotificacao": "https://valpagtesouro.tesouro.gov.br/api/simulador/ug/notificacao"
        }

    def get_index_request(self):
        url = self.getBaseUrl() + '/'

        response = requests.get(url, headers=self.getHeaders())

        if response.status_code == HTTPStatus.OK:
            return response.json()
        else:
            # Trate os erros de acordo com suas necessidades
            raise Exception(f'Erro na requisição GET: {response.status_code}')

    def post_solicitacao_pagamento(self, request, sanitize=True):
        url = self.getBaseUrl() + '/gru/solicitacao-pagamento'

        if (sanitize):
            data = self.getSanitizedData(request)
        else:
            data = request

        response = requests.post(url, headers=self.getHeaders(), data=data)

        if response.status_code == HTTPStatus.CREATED:
            return response.json()
        else:
            # Trate os erros de acordo com suas necessidades
            raise Exception(f'Erro na requisição GET: {response.status_code}')
