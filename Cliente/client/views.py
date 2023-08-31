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

    def __init__(self, pagtesouro_servico, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.pagtesouro_servico = pagtesouro_servico

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {"show_form": True})

    def post(self, request, *args, **kwargs):
        result_dict = {
            "show_form": False, 
            "show_post_msg": True, 
            "pagamento": {
                "idPagamento": "1123jklfdsFhf",
                "sessao": "12345-456789-456456-456456"
            }
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
