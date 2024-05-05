# views.py
from rest_framework import generics, permissions
from .models import Flight
from .serializers import FlightSerializer

class FlightListCreateAPIView(generics.ListCreateAPIView):
    queryset = Flight.objects.all()
    serializer_class = FlightSerializer
    permission_classes = [permissions.IsAuthenticated]

class FlightRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Flight.objects.all()
    serializer_class = FlightSerializer
    permission_classes = [permissions.IsAuthenticated]


class FlightSearchAPIView(generics.ListAPIView):
    serializer_class = FlightSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Retrieve query parameters from request
        departure_location = self.request.query_params.get('departure_location')
        arrival_location = self.request.query_params.get('arrival_location')
        departure_time = self.request.query_params.get('departure_time')
        flight_class = self.request.query_params.get('flight_class')

        # Perform filtering based on query parameters
        queryset = Flight.objects.filter(
            departure_location__airport_name=departure_location,
            arrival_location__airport_name=arrival_location,
            departure_datetime__date=departure_time,
        )

        return queryset
    
class RoundTripFlightSearchAPIView(generics.ListAPIView):
    serializer_class = FlightSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Retrieve query parameters from request
        departure_location = self.request.query_params.get('departure_location')
        arrival_location = self.request.query_params.get('arrival_location')
        departure_time = self.request.query_params.get('departure_time')
        flight_class = self.request.query_params.get('flight_class')

        # Perform filtering for outbound flights
        outbound_flights = Flight.objects.filter(
            departure_location__airport_name=departure_location,
            arrival_location__airport_name=arrival_location,
            departure_datetime__date=departure_time,
        )

        # Perform filtering for return flights
        return_flights = Flight.objects.filter(
            departure_location__airport_name=arrival_location,
            arrival_location__airport_name=departure_location,
            departure_datetime__gte=departure_time,  # Assuming return flight departs after outbound flight
        )

        # Return pairs of outbound and return flights
        return zip(outbound_flights, return_flights)
