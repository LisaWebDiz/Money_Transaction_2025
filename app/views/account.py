from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from app.serializers.account import AccountSerializer


class AccountViewSet(viewsets.ViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['get'])
    def my_account(self, request):
        account = request.user.user_account
        serializer = AccountSerializer(account)
        return Response(serializer.data)
