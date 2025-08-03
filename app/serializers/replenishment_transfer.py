from decimal import Decimal

from rest_framework import serializers


class ReplenishmentSerializer(serializers.Serializer):
    # Принимаем в копейках: 1 = 0.01 рубля
    amount = serializers.IntegerField(min_value=1)

class TransferSerializer(serializers.Serializer):
    # Переводим в рублях: 0.01 = 1 копейка
    amount = serializers.DecimalField(max_digits=20, decimal_places=2, min_value=Decimal('0.01'))
    receiver_id = serializers.IntegerField()
