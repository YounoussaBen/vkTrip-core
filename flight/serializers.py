from rest_framework import serializers
from .models import Flight, Stepover, Location

class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        read_only_fields = ["id", "created", "updated"]
        fields = ['airport_name', 'country']

class StepoverSerializer(serializers.ModelSerializer):
    location = LocationSerializer()

    class Meta:
        model = Stepover
        read_only_fields = ["id", "created", "updated"]
        fields = ['location', 'duration']

class FlightSerializer(serializers.ModelSerializer):
    departure_location = LocationSerializer()
    arrival_location = LocationSerializer()
    stepovers = StepoverSerializer(many=True)
    num_tickets = serializers.IntegerField(write_only=True, required=True)  # New field for number of tickets

    class Meta:
        model = Flight
        read_only_fields = ["id", "created", "updated"]
        fields = ['departure_location', 'arrival_location', 'departure_datetime',
                  'return_datetime', 'base_price', 'checked_bag_price', 'stepovers', 'num_tickets']

    def create(self, validated_data):
        num_tickets = validated_data.pop('num_tickets')  # Pop out num_tickets field
        flight = Flight.objects.create(**validated_data)

        # Create the specified number of tickets for the flight
        for _ in range(num_tickets):
            flight.tickets.create()

        return flight
