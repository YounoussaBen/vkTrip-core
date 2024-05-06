from rest_framework import serializers
from .models import Payment

class PaymentSerializer(serializers.ModelSerializer):
    payment_method = serializers.CharField(default='Card') # Default payment method is Card
    booking_id = serializers.UUIDField()
    class Meta:
        model = Payment
        read_only_fields = ['timestamp', 'created_at', 'updated_at', 'user', 'payment_method']
        exclude = ['is_deleted', 'payment_status']