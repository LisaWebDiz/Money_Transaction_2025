from decimal import Decimal

from django.db.models import Q
from drf_spectacular.utils import extend_schema
from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response

from app.models import Operation
from app.serializers.operation import OperationSerializer
from app.serializers.replenishment_transfer import ReplenishmentSerializer, TransferSerializer
from app.services.replenishment import replenishment
from app.services.transfer import transfer


class OperationViewSet(viewsets.ModelViewSet):
    serializer_class = OperationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Operation.objects.filter(
            Q(sender=user) | Q(receiver=user)
        ).order_by('-timestamp')

    @extend_schema(
        summary='Мои операции',
        description='Получить список всех операций текущего залогиненного пользователя',
        responses={200: OperationSerializer(many=True)}
    )
    @action(detail=False, methods=['get'], url_path='my_operations')
    def my_operations(self, request):
        user = request.user
        operations = Operation.objects.filter(
            Q(sender=user) | Q(receiver=user)
        ).order_by('-timestamp')
        serializer = self.get_serializer(operations, many=True)
        return Response(serializer.data)


    @extend_schema(
        summary='Пополнение в копейках',
        request=ReplenishmentSerializer,
        responses=OperationSerializer
    )
    @action(detail=False, methods=['post'])
    def replenish(self, request):
        serializer = ReplenishmentSerializer(data=request.data)
        if serializer.is_valid():
            try:
                amount = serializer.validated_data['amount']
                op = replenishment(request.user.id, Decimal(amount))
                return Response(OperationSerializer(op).data)
            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        request=TransferSerializer,
        responses=OperationSerializer,
        summary='Перевод средств другому пользователю',
        description='Позволяет перевести средства на счёт другого пользователя по его ID'
    )

    @action(detail=False, methods=['post'])
    def transfer(self, request):
        serializer = TransferSerializer(data=request.data)
        if serializer.is_valid():
            try:
                amount = Decimal(request.data.get('amount'))
                receiver_id = int(request.data.get('receiver_id'))
                op = transfer(request.user.id, receiver_id, amount)
                return Response(OperationSerializer(op).data)
            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
