from django.urls import path
from .views import PaginaInicial

urlpatterns = [
    path('', PaginaInicial.as_view(), name="index")
]