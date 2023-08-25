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
    GruPagamentoAPIView
)

router = routers.DefaultRouter()
#router.register(r'/', HomeApiView)
router.register(r'users', UserViewSet)
router.register(r'groups', GroupViewSet)

urlpatterns = [
    path('gru/pagamento/', GruPagamentoAPIView.as_view(), name='gru_pagamento'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('', HomeApiView.as_view()),
    path('', include(router.urls)),
]