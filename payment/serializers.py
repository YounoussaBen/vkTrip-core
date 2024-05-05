import datetime

from rest_framework import serializers


class CheckExpiryMonth:
    def __call__(self, value):
        if not 1 <= int(value) <= 12:
            raise serializers.ValidationError("Invalid expiry month.")

class CheckExpiryYear:
    def __call__(self, value):
        today = datetime.datetime.now()
        if not int(value) >= today.year:
            raise serializers.ValidationError("Invalid expiry year.")

class CheckCVC:
    def __call__(self, value):
        if not 3 <= len(value) <= 4:
            raise serializers.ValidationError("Invalid cvc number.")

class CheckPaymentMethod:
    def __call__(self, value):
        payment_method = value.lower()
        if payment_method not in ["card"]:
            raise serializers.ValidationError("Invalid payment_method.")

class CardInformationSerializer(serializers.Serializer):
    card_number = serializers.CharField(max_length=150, required=True)
    expiry_month = serializers.CharField(max_length=2, required=True, validators=[CheckExpiryMonth()])
    expiry_year = serializers.CharField(max_length=4, required=True, validators=[CheckExpiryYear()])
    cvc = serializers.CharField(max_length=4, required=True, validators=[CheckCVC()])
    card_token = serializers.CharField(max_length=150, required=True)  # Add card_token field
