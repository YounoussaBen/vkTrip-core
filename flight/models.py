from django.db import models
from base.models import BaseModel


class Location(BaseModel):
    airport_name = models.CharField(max_length=100)
    country = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.airport_name} ({self.country})"

class Flight(BaseModel):
    departure_location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name='departures')
    arrival_location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name='arrivals', null=True, blank=True)
    departure_datetime = models.DateTimeField()
    return_datetime = models.DateTimeField(null=True, blank=True)
    base_price = models.DecimalField(max_digits=10, decimal_places=2)
    checked_bag_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)  # Added field for checked bag price

    @property
    def available_tickets(self):
        return self.tickets.filter(is_booked=False).count()

class Ticket(BaseModel):
    flight = models.ForeignKey(Flight, on_delete=models.CASCADE, related_name='tickets')
    is_booked = models.BooleanField(default=False)

class Stepover(BaseModel):
    flight = models.ForeignKey(Flight, on_delete=models.CASCADE, related_name='stepovers')
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    duration = models.DurationField()