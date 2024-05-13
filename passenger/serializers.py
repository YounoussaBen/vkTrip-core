from rest_framework import serializers
from .models import Passenger, EmergencyContact


class EmergencyContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmergencyContact
        read_only_fields = ["id", "created", "updated"]
        fields = ['FullName', 'Email', 'PhoneNumber']


class PassengerSerializer(serializers.ModelSerializer):
    EmergencyContact = EmergencyContactSerializer(required=False)

    class Meta:
        model = Passenger
        read_only_fields = ["id", "created", "updated"]
        exclude = ["is_deleted"]

    def create(self, validated_data):
        emergency_contact_data = validated_data.pop('EmergencyContact', None)
        passenger = Passenger.objects.create(**validated_data)
        if emergency_contact_data:
            EmergencyContact.objects.create(Passenger=passenger, **emergency_contact_data)
        return passenger