from urllib.parse import urlparse, parse_qs
from .models import Pagamento

class Taxas:
    id = 0
    nome = ''
    valor = 0.00

    def __init__(self, id=0, nome='', valor=0.00):
        self.id = id
        self.nome = nome
        self.valor = valor

    def __str__(self):
        valorStr = 'R$ ' + str(self.valor)

        if self.valor < 1.00:
            valorStr = 'Isento'

        return "{} ({})".format(self.nome, valorStr)

class HelperService:
    def getVestibularTaxas(self):
        return [
            Taxas(id=1, nome='Categoria A', valor=75.0),
            Taxas(id=2, nome='Categoria A', valor=145.0),
            Taxas(id=3, nome='Categoria C')
        ]

    def getIdSessaoFromUrl(self, url):
        # Parse da URL
        parsed_url = urlparse(url)

        # Obtém os parâmetros da query string
        query_params = parse_qs(parsed_url.fragment)

        # Obtém o valor de 'idSessao' se estiver presente
        chave = '/pagamento?idSessao'
        if chave in query_params:
            return query_params[chave][0]
        else:
            return ''

    def savePagamentoModelFromApiResponse(self, payload, api_response):
        pagamento = Pagamento()

        pagamento.idPagamento = api_response["idPagamento"]
        pagamento.idSessao = self.getIdSessaoFromUrl(api_response['proximaUrl'])
        pagamento.codigoServico = payload['codigoServico']
        pagamento.referencia = payload['referencia']
        pagamento.competencia = payload['competencia']
        pagamento.vencimento = payload['vencimento']
        pagamento.cnpjCpf = payload['cnpjCpf']
        pagamento.nomeContribuinte = payload['nomeContribuinte']
        pagamento.valorPrincipal = payload['valorPrincipal']
        pagamento.valorDescontos = payload['valorDescontos']
        pagamento.valorOutrasDeducoes = payload['valorOutrasDeducoes']
        pagamento.valorMulta = payload['valorMulta']
        pagamento.valorJuros = payload['valorJuros']
        pagamento.valorOutrosAcrescimos = payload['valorOutrosAcrescimos']
        pagamento.modoNavegacao = payload['modoNavegacao']
        pagamento.urlNotificacao = payload['urlNotificacao']
        pagamento.dataCriacao = api_response['dataCriacao']
        pagamento.proximaUrl = api_response['proximaUrl']
        pagamento.tipoPagamentoEscolhido = ''
        pagamento.nomePSP = ''
        pagamento.transacaoPSP = ''
        pagamento.situacao_codigo = api_response['situacao']['codigo']
        pagamento.situacao_dataHora = api_response['dataCriacao']

        pagamento.save()
        return pagamento
