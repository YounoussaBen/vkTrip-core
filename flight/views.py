# views.py
from rest_framework import generics, permissions
from .models import Flight, Location
from .serializers import FlightSerializer, LocationSerializer
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from datetime import datetime
from django.db.models import Q


class FlightListCreateAPIView(generics.ListCreateAPIView):
    queryset = Flight.objects.all()
    serializer_class = FlightSerializer
    permission_classes = [permissions.IsAuthenticated]


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

        queryset = Flight.objects.filter(
            Q(departure_location__airport_name=departure_location) &
            Q(arrival_location__airport_name=arrival_location) &
            Q(departure_datetime__date=departure_time) &
            Q(flight_class=flight_class) &
            Q(passenger_type=passenger_type)
        ) | Flight.objects.filter(
            Q(departure_location__airport_name=arrival_location) &
            Q(arrival_location__airport_name=departure_location) &
            Q(departure_datetime__date=return_time) &
            Q(flight_class=flight_class) &
            Q(passenger_type=passenger_type)
        )

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

        queryset = Flight.objects.all()

        if departure_location:
            queryset = queryset.filter(departure_location__airport_name=departure_location)
        if arrival_location:
            queryset = queryset.filter(arrival_location__airport_name=arrival_location)
        if departure_time:
            departure_time = datetime.strptime(departure_time, '%Y-%m-%d')
            queryset = queryset.filter(departure_datetime__date=departure_time.date())
        if flight_class:
            queryset = queryset.filter(flight_class=flight_class)
        if passenger_type:
            queryset = queryset.filter(passenger_type=passenger_type)

        return queryset


class FlightRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Flight.objects.all()
    serializer_class = FlightSerializer
    permission_classes = [permissions.AllowAny]

class LocationListAPIView(generics.ListAPIView):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer
    permission_classes = [permissions.AllowAny]
