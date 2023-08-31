from django.urls import path
from .views import (
    PaginaInicial,
    CadastrarPagamentoView,
    ConsultarPagamentoView,
    ExibirPagamentoView,
)
from .pagtesouro_service import PagTesouroService

urlpatterns = [
    path('', PaginaInicial.as_view(pagtesouro_servico=PagTesouroService()), name="index"),
    path('create/', CadastrarPagamentoView.as_view(pagtesouro_servico=PagTesouroService()), name="create"),
    path('query/', ConsultarPagamentoView.as_view(pagtesouro_servico=PagTesouroService()), name="query"),
    path('<str:id_pagamento>/', ExibirPagamentoView.as_view(pagtesouro_servico=PagTesouroService()), name="show"),
]