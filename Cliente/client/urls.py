from django.urls import path
from .views import (
    PaginaInicial,
    CadastrarPagamentoView,
    ConsultarPagamentoView,
    ExibirPagamentoView,
    ReceberNotificacaoPagamentoView,
)
from .pagtesouro_service import PagTesouroService
from .helper_service import HelperService

urlpatterns = [
    path('', PaginaInicial.as_view(pagtesouro_servico=PagTesouroService()), name="index"),
    path('create/', CadastrarPagamentoView.as_view(pagtesouro_servico=PagTesouroService(),helper_servico=HelperService()), name="create"),
    path('query/', ConsultarPagamentoView.as_view(pagtesouro_servico=PagTesouroService()), name="query"),
    path('notificacao/', ReceberNotificacaoPagamentoView.as_view(), name="notificacao"),
    path('<str:id_pagamento>/', ExibirPagamentoView.as_view(pagtesouro_servico=PagTesouroService()), name="show"),
]
