from rest_framework import serializers


class ReplenishmentSerializer(serializers.Serializer):
    amount = serializers.IntegerField(min_value=1)

class TransferSerializer(serializers.Serializer):
    amount = serializers.IntegerField(min_value=1)
    receiver_id = serializers.IntegerField()
