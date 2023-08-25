from django.contrib.auth.models import User, Group
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import (viewsets, permissions)
from rest_framework.status import (
    HTTP_200_OK, HTTP_201_CREATED, HTTP_400_BAD_REQUEST
)
from .serializers import (
    UserSerializer, 
    GroupSerializer,
    GruPagamentoSerializer,
)

class HomeApiView(APIView):
    def get(self, request, format=None):
        return Response({"nome":"PagTesouro Simulador API", "version":"1.0"}, status=200)

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]

class GruPagamentoAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request, format=None):
        serializer = GruPagamentoSerializer(data=request.data)

        return Response(serializer.initial_data, status=HTTP_200_OK)