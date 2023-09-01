from django.db import models

# Create your models here.
class Pagamento(models.Model):
    idPagamento = models.CharField(max_length=255, null=True, blank=True, verbose_name="id do pagamento")
    idSessao = models.CharField(max_length=255, null=True, blank=True, verbose_name="id da sessão do pagamento")
    codigoServico = models.CharField(max_length=255, null=True, blank=True, verbose_name="Código do Serviço")
    referencia = models.CharField(max_length=255, null=True, blank=True, verbose_name="Número de referência da GRU")
    competencia = models.CharField(max_length=255, null=True, blank=True, verbose_name="Competência (mês e ano)")
    vencimento = models.CharField(max_length=255, null=True, blank=True, verbose_name="Vencimento da GRU, se houver")
    cnpjCpf = models.CharField(max_length=255, null=True, blank=True, verbose_name="CPF ou CNPJ")
    nomeContribuinte = models.CharField(max_length=255, null=True, blank=True, verbose_name="Nome do contribuinte")
    valorPrincipal = models.CharField(max_length=255, null=True, blank=True, verbose_name="Valor Principal")
    valorDescontos = models.CharField(max_length=255, null=True, blank=True, verbose_name="Desconto")
    valorOutrasDeducoes = models.CharField(max_length=255, null=True, blank=True, verbose_name="Outras deduções")
    valorMulta = models.CharField(max_length=255, null=True, blank=True, verbose_name="Multa")
    valorJuros = models.CharField(max_length=255, null=True, blank=True, verbose_name="Juros")
    valorOutrosAcrescimos = models.CharField(max_length=255, null=True, blank=True, verbose_name="Outros Acrescimos")
    modoNavegacao = models.CharField(max_length=255, null=True, blank=True, verbose_name="Modo Navegação")
    urlNotificacao = models.CharField(max_length=255, null=True, blank=True, verbose_name="URL Notificacao")
    dataCriacao = models.CharField(max_length=255, null=True, blank=True, verbose_name="Data de criação")
    proximaUrl = models.CharField(max_length=255, null=True, blank=True, verbose_name="Próxima URL")
    tipoPagamentoEscolhido = models.CharField(max_length=255, null=True, blank=True, verbose_name="Tipo de Pagamento")
    nomePSP = models.CharField(max_length=255, null=True, blank=True, verbose_name="Nome do PSP")
    transacaoPSP = models.CharField(max_length=255, null=True, blank=True, verbose_name="Identificação do pagamento no PSP")
    situacao_codigo = models.CharField(max_length=255, null=True, blank=True, verbose_name="Situação do pagamento")
    situacao_dataHora = models.CharField(max_length=255, null=True, blank=True, verbose_name="Atualização da situação do pgamento")

    def __str__(self):
        return "{} - {} ({})".format(self.idPagamento, self.dataCriacao, self.situacao_codigo)

    def getTotalValores(self):
        totalPositivo = float(self.valorPrincipal) + float(self.valorMulta)  + float(self.valorJuros) + float(self.valorOutrosAcrescimos)
        totalNegativo = float(self.valorDescontos) + float(self.valorOutrasDeducoes)

        return totalPositivo - totalNegativo
