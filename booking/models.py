from django.db import models
from base.models import BaseModel
from passenger.models import Passenger
from flight.models import Flight
from account.models import User


class Booking(BaseModel):
    ROUND_TRIP = 'Round Trip'
    ONE_WAY = 'One Way'
    TRIP_TYPE_CHOICES = (
        (ROUND_TRIP, 'Round Trip'),
        (ONE_WAY, 'One Way'),
    )
    trip_type = models.CharField(max_length=20, choices=TRIP_TYPE_CHOICES)


    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    passengers = models.ManyToManyField(Passenger, related_name='bookings')
    flights = models.ManyToManyField(Flight, related_name='bookings')
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    checked_bags = models.PositiveIntegerField(default=0)