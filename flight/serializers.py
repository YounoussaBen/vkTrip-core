from rest_framework import serializers
from .models import Flight, Stopover, Location, Airline

class AirlineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Airline
        read_only_fields = [ "created", "updated"]
        fields = ["id", 'name', 'logo']
class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        read_only_fields = [ "created", "updated"]
        fields = ["id", 'airport_name', 'country']

class StepoverSerializer(serializers.ModelSerializer):
    location = LocationSerializer()

    class Meta:
        model = Stopover
        read_only_fields = [ "created", "updated"]
        fields = ["id", 'location', 'duration']

class FlightSerializer(serializers.ModelSerializer):
    departure_location = LocationSerializer()
    arrival_location = LocationSerializer()
    stepovers = StepoverSerializer(many=True)
    airline = AirlineSerializer()
    num_tickets = serializers.IntegerField(write_only=True, required=True)  # New field for number of tickets

    class Meta:
        model = Flight
        read_only_fields = [ "created", "updated"]
        fields = ["id", 'airline','departure_location', 'arrival_location', 'departure_datetime',
                    'base_price', 'passenger_type', 'flight_class', 'checked_bag_price', 'stepovers', 'num_tickets', 'available_tickets']

    def create(self, validated_data):
        num_tickets = validated_data.pop('num_tickets')  # Pop out num_tickets field
        flight = Flight.objects.create(**validated_data)

        # Create the specified number of tickets for the flight
        for _ in range(num_tickets):
            flight.tickets.create()

        return flight
