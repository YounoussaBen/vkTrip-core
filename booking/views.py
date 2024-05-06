from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import Booking
from .serializers import BookingSerializer
from flight.models import Flight
from django.db.models import F

class BookingListCreateView(generics.ListCreateAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Booking.objects.filter(created_by=self.request.user)

    def perform_create(self, serializer):
        booking_instance = serializer.save(created_by=self.request.user)
        for flight in booking_instance.flights.all():
            Flight.objects.filter(pk=flight.pk, tickets__is_booked=True).update(tickets=F('tickets') - 1)

class BookingRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Booking.objects.filter(created_by=self.request.user)
    
class UserBookingListView(generics.ListAPIView):
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Filter bookings based on the currently authenticated user
        return Booking.objects.filter(created_by=self.request.user)