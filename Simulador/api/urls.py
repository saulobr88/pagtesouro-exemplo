from django.urls import path, include
from rest_framework import routers
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)
from .views import (
    HomeApiView, 
    UserViewSet, 
    GroupViewSet,
    GruPagamentoAPIView,
    GruPagamentoNotificacaoAPIView,
    GruPagamentoConsultaAPIView,
)

router = routers.DefaultRouter()
#router.register(r'/', HomeApiView)
router.register(r'users', UserViewSet)
router.register(r'groups', GroupViewSet)

urlpatterns = [
    path('gru/solicitacao-pagamento', GruPagamentoAPIView.as_view(), name='gru_pagamento'),
    path('gru/pagamento/notificacao', GruPagamentoNotificacaoAPIView.as_view(), name='gru_pagamento_notificacao'),
    path('gru/pagamentos/<str:id_pagamento>', GruPagamentoConsultaAPIView.as_view(), name='gru_pagamento_consulta'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('', HomeApiView.as_view()),
    path('', include(router.urls)),
]