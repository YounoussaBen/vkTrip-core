from django.db import models
from base.models import BaseModel
from datetime import timedelta

class Location(BaseModel):
    airport_name = models.CharField(max_length=100)
    country = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.airport_name} ({self.country})"

class Airline(BaseModel):
    name = models.CharField(max_length=100)
    logo = models.ImageField(upload_to='airline_logos/', null=True, blank=True)

    def __str__(self):
        return self.name

class Flight(BaseModel):
    airline = models.ForeignKey(Airline, on_delete=models.CASCADE, related_name='flights')
    departure_location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name='departures')
    arrival_location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name='arrivals')
    departure_datetime = models.DateTimeField()
    flight_duration = models.DurationField(default=timedelta(days=0))
    base_price = models.DecimalField(max_digits=10, decimal_places=2)
    
    MINOR = 'Minor'
    ADULT = 'Adult'
    PASSENGER_CHOICES = (
        (MINOR, 'Minor'),
        (ADULT, 'Adult'),
    )
    passenger_type = models.CharField(max_length=100, choices=PASSENGER_CHOICES, default=ADULT)

    BUSINESS_CLASS = 'Business'
    ECONOMIC_CLASS = 'Economic'
    CLASS_CHOICES = (
        (BUSINESS_CLASS, 'Business Class'),
        (ECONOMIC_CLASS, 'Economic Class'),
    )
    flight_class = models.CharField(max_length=20, choices=CLASS_CHOICES, default=ECONOMIC_CLASS)

    checked_bag_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    @property
    def available_tickets(self):
        return self.tickets.filter(is_booked=False).count()

class Ticket(BaseModel):
    flight = models.ForeignKey(Flight, on_delete=models.CASCADE, related_name='tickets')
    is_booked = models.BooleanField(default=False)

class Stopover(BaseModel):
    flight = models.ForeignKey(Flight, on_delete=models.CASCADE, related_name='stopovers')
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    duration = models.DurationField()
