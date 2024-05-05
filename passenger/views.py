from rest_framework import generics
from .models import Passenger
from .serializers import PassengerSerializer
from rest_framework.permissions import IsAuthenticated


class PassengerListCreateAPIView(generics.ListCreateAPIView):
    queryset = Passenger.objects.all()
    serializer_class = PassengerSerializer
    permission_classes = [IsAuthenticated]


class PassengerRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Passenger.objects.all()
    serializer_class = PassengerSerializer
    permission_classes = [IsAuthenticated]