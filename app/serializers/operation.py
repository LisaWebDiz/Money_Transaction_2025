from rest_framework import serializers

from app.models import Operation


class OperationSerializer(serializers.ModelSerializer):
    type_display = serializers.CharField(source='get_type_display', read_only=True)

    class Meta:
        model = Operation
        fields = ['sender', 'receiver', 'type', 'type_display', 'amount', 'timestamp', 'resulting_balance']
        read_only_fields = ['sender', 'receiver', 'type', 'timestamp']

    def get_type_display(self, obj):
        return obj.get_type_display()
