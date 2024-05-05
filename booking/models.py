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

    BUSINESS_CLASS = 'Business'
    ECONOMIC_CLASS = 'Economic'
    CLASS_CHOICES = (
        (BUSINESS_CLASS, 'Business Class'),
        (ECONOMIC_CLASS, 'Economic Class'),
    )
    flight_class = models.CharField(max_length=20, choices=CLASS_CHOICES)

    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    passengers = models.ManyToManyField(Passenger, related_name='bookings')
    flights = models.ManyToManyField(Flight, related_name='bookings')
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    completed = models.BooleanField(default=False)
    checked_bags = models.PositiveIntegerField(default=0)

    def save(self, *args, **kwargs):
        if self.trip_type and self.flight_class and self.passengers.exists() and self.flights.exists():
            self.completed = True
            total_price = 0
            for flight in self.flights.all():
                base_price = flight.base_price
                if self.flight_class == self.BUSINESS_CLASS:
                    base_price *= 1.5
                elif self.flight_class == self.ECONOMIC_CLASS:
                    base_price *= 1

                for passenger in self.passengers.all():
                    if passenger.age() < 16:
                        base_price *= 0.8

                if self.trip_type == self.ROUND_TRIP:
                    base_price *= 2

                # Retrieve checked bag price from associated flight
                checked_bag_price = flight.checked_bag_price

                # Adjust price based on checked bags
                if self.flight_class == self.ECONOMIC_CLASS:
                    checked_bags_price = checked_bag_price * self.checked_bags
                    base_price += checked_bags_price
                elif self.flight_class == self.BUSINESS_CLASS:
                    if self.checked_bags > 2:
                        checked_bags_price = checked_bag_price * (self.checked_bags - 2)
                        base_price += checked_bags_price

                total_price += base_price

            self.total_price = total_price
        else:
            self.completed = False

        super().save(*args, **kwargs)