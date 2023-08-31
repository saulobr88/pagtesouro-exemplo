from django.shortcuts import render
from django.views.generic import TemplateView

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

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)

class ExibirPagamentoView(TemplateView):
    template_name = 'client/pagamentos/show.html'
    pagtesouro_servico = None

    def __init__(self, pagtesouro_servico, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.pagtesouro_servico = pagtesouro_servico

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
