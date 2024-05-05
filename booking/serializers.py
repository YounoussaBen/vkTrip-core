from rest_framework import serializers
from .models import Booking

class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        read_only_fields = ["id", "created", "updated", "created_by"]
        exclude = ["is_deleted"]
    