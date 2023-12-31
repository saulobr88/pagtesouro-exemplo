import json
from django.shortcuts import render
from django.views.generic import TemplateView
from django.http import JsonResponse
from django.views import View
from django.http import Http404
from django.db import models
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from .models import Pagamento

# Create your views here.
class PaginaInicial(TemplateView):
    # Toda classe filha do TemplateView precisa do
    # atributo abaixo para definir um template a ser renderizado
    template_name = 'client/index.html'
    pagtesouro_servico = None

    def __init__(self, pagtesouro_servico, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.pagtesouro_servico = pagtesouro_servico

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)

        if (self.pagtesouro_servico):
            context["api_info"] = self.pagtesouro_servico.get_index_request()
        else:
            context["api_info"] = {"nome": "Null", "version": "0.0"}
        return context

class CadastrarPagamentoView(TemplateView):
    template_name = 'client/pagamentos/create.html'
    pagtesouro_servico = None
    helper_servico = None

    def __init__(self, pagtesouro_servico, helper_servico, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.pagtesouro_servico = pagtesouro_servico
        self.helper_servico = helper_servico

    def get(self, request, *args, **kwargs):
        result_dict = {
            "show_form": True,
            "taxas": self.helper_servico.getVestibularTaxas(),
        }
        return render(request, self.template_name, result_dict)

    def post(self, request, *args, **kwargs):

        input = request.POST.items()
        dataSanitized = self.pagtesouro_servico.getSanitizedData(request)

        api_response = self.pagtesouro_servico.post_solicitacao_pagamento(dataSanitized, sanitize=False)

        pagamento = None
        if (api_response):
            pagamento = self.helper_servico.savePagamentoModelFromApiResponse(payload=dataSanitized, api_response=api_response)

        if (pagamento):
            result_dict = {
                "show_form": False,
                "show_post_msg": True,
                "pagamento": {
                    "idPagamento": str(pagamento.idPagamento),
                    "sessao": str(pagamento.idSessao)
                },
                "input": input
            }
        else:
            result_dict = {
                "show_form": True,
                "show_post_msg": True,
                "pagamento": {
                    "idPagamento": "Erro",
                    "sessao": "Erro"
                },
                "input": input
            }

        return render(request, self.template_name, result_dict)


class ConsultarPagamentoView(TemplateView):
    template_name = 'client/pagamentos/query.html'
    pagtesouro_servico = None

    def __init__(self, pagtesouro_servico, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.pagtesouro_servico = pagtesouro_servico

    def get(self, request):
        # Obtém o parâmetro 'q' da URL
        q = request.GET.get('q')

        # Realiza a consulta no banco de dados para buscar Pagamentos que correspondem ao 'q'
        if not q:
            q = '#########'

        pagamentos = Pagamento.objects.filter(models.Q(cnpjCpf__icontains=q) | models.Q(idPagamento__icontains=q))

        # Renderiza o template com os resultados da consulta
        return render(request, self.template_name, {'pagamentos': pagamentos})

class ExibirPagamentoView(TemplateView):
    template_name = 'client/pagamentos/show.html'
    pagtesouro_servico = None

    def __init__(self, pagtesouro_servico, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.pagtesouro_servico = pagtesouro_servico

    def get(self, request, id_pagamento):
        pagamento = None
        if id_pagamento:
            try:
                pagamento = Pagamento.objects.get(idPagamento=id_pagamento)
            except Exception as e:
                pagamento = None

        if (pagamento and pagamento.refetch):
            pagamentoJson = self.pagtesouro_servico.get_consulta_pagamento(pagamento.idPagamento)
            pagamento.tipoPagamentoEscolhido = pagamentoJson['tipoPagamentoEscolhido']
            pagamento.nomePSP = pagamentoJson['nomePSP']
            pagamento.transacaoPSP = pagamentoJson['transacaoPSP']
            pagamento.situacao_codigo = pagamentoJson['situacao']['codigo']
            pagamento.situacao_dataHora = pagamentoJson['situacao']['data']
            pagamento.refetch = False
            pagamento.save()

        return render(request, self.template_name, {'pagamento': pagamento})


class ReceberNotificacaoPagamentoView(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def post(self, request):
        # Parse do JSON da requisição
        try:
            data = json.loads(request.body)
            id_pagamento = data.get('idPagamento')
        except json.JSONDecodeError:
            return JsonResponse({"mensagem": "Requisição JSON inválida."}, status=400)

        # Verifique se existe um Pagamento com o idPagamento informado
        try:
            pagamento = Pagamento.objects.get(idPagamento=id_pagamento)
            pagamento.situacao_dataHora = data.get('dataHora')
            pagamento.refetch = True
            pagamento.save()

            print('Pagamento após o save')
            print(pagamento)

            return JsonResponse({"mensagem": "Pagamento encontrado.", "pagamento": pagamento.idPagamento}, status=200)
        except Pagamento.DoesNotExist:
            return JsonResponse([{"codigo": 404, "descricao":"Pagamento não encontrado."}], status=404)
