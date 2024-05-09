# views.py
from rest_framework import generics, permissions
from .models import Flight, Location, Airline
from .serializers import FlightSerializer, LocationSerializer, AirlineSerializer
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from datetime import datetime
from django.db.models import Q
from itertools import chain

class FlightListCreateAPIView(generics.ListCreateAPIView):
    queryset = Flight.objects.all()
    serializer_class = FlightSerializer
    permission_classes = [permissions.AllowAny]
    
    def get_queryset(self):
        return Flight.objects.filter(tickets__is_booked=False).distinct()

class RoundTripFlightSearchAPIView(generics.ListAPIView):
    serializer_class = FlightSerializer
    permission_classes = [permissions.AllowAny]

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('departure_location', openapi.IN_QUERY, description="Departure location", type=openapi.TYPE_STRING, example="Lagos", required=True),
            openapi.Parameter('arrival_location', openapi.IN_QUERY, description="Arrival location", type=openapi.TYPE_STRING, example="Abuja", required=True),
            openapi.Parameter('departure_time', openapi.IN_QUERY, description="Departure time (format: 'YYYY-MM-DD')", type=openapi.TYPE_STRING, example="2021-12-31", required=True),
            openapi.Parameter('return_time', openapi.IN_QUERY, description="Return time (format: 'YYYY-MM-DD')", type=openapi.TYPE_STRING, example="2021-12-31", required=True),
            openapi.Parameter('flight_class', openapi.IN_QUERY, description="Flight class", type=openapi.TYPE_STRING, example="Economic", required=True),
            openapi.Parameter('passenger_type', openapi.IN_QUERY, description="Passenger type", type=openapi.TYPE_STRING, example="Adult", required=True),
        ]
    )
    def get_queryset(self):
        departure_location = self.request.query_params.get('departure_location')
        arrival_location = self.request.query_params.get('arrival_location')
        departure_time = self.request.query_params.get('departure_time')
        return_time = self.request.query_params.get('return_time')
        flight_class = self.request.query_params.get('flight_class')
        passenger_type = self.request.query_params.get('passenger_type')

        # Filter outbound flights
        outbound_flights = Flight.objects.filter(
            departure_location__airport_name=departure_location,
            arrival_location__airport_name=arrival_location,
            departure_datetime__date=departure_time,
            flight_class=flight_class,
            passenger_type=passenger_type,
            tickets__is_booked=False
        )

        # Filter return flights
        return_flights = Flight.objects.filter(
            departure_location__airport_name=arrival_location,
            arrival_location__airport_name=departure_location,
            departure_datetime__date=return_time,
            flight_class=flight_class,
            passenger_type=passenger_type,
            tickets__is_booked=False
        )

        # Combine both outbound and return flights
        queryset = list(chain(outbound_flights, return_flights))

        return queryset

class FlightSearchAPIView(generics.ListAPIView):
    serializer_class = FlightSerializer
    permission_classes = [permissions.AllowAny]

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('departure_location', openapi.IN_QUERY, description="Departure location", type=openapi.TYPE_STRING, example="Lagos", required=True),
            openapi.Parameter('arrival_location', openapi.IN_QUERY, description="Arrival location", type=openapi.TYPE_STRING, example="Abuja", required=True),
            openapi.Parameter('departure_time', openapi.IN_QUERY, description="Departure time (format: 'YYYY-MM-DD')", type=openapi.TYPE_STRING, example="2021-12-31", required=True),
            openapi.Parameter('flight_class', openapi.IN_QUERY, description="Flight class", type=openapi.TYPE_STRING, example="Economic", required=True),
            openapi.Parameter('passenger_type', openapi.IN_QUERY, description="Passenger type", type=openapi.TYPE_STRING, example="Adult", required=True),
        ]
    )
    def get_queryset(self):
        departure_location = self.request.query_params.get('departure_location')
        arrival_location = self.request.query_params.get('arrival_location')
        departure_time = self.request.query_params.get('departure_time')
        flight_class = self.request.query_params.get('flight_class')
        passenger_type = self.request.query_params.get('passenger_type')

        # Filter flights based on all mandatory parameters
        queryset = Flight.objects.filter(
            departure_location__airport_name=departure_location,
            arrival_location__airport_name=arrival_location,
            departure_datetime__date=datetime.strptime(departure_time, '%Y-%m-%d').date(),
            flight_class=flight_class,
            passenger_type=passenger_type,
        )

        # Filter out flights with zero available tickets
        queryset = queryset.filter(tickets__is_booked=False).distinct()

        return queryset


class FlightRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Flight.objects.all()
    serializer_class = FlightSerializer
    permission_classes = [permissions.AllowAny]

class LocationListAPIView(generics.ListAPIView):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer
    permission_classes = [permissions.AllowAny]
