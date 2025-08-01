from rest_framework import serializers

from app.models import Operation


class OperationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Operation
        fields = ['sender', 'receiver', 'type', 'amount', 'timestamp', 'resulting_balance']
        read_only_fields = ['sender', 'receiver', 'type', 'timestamp']
