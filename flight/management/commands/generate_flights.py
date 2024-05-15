# generate_random_flights.py

import random
import datetime
from faker import Faker
from django.core.management.base import BaseCommand
from django.db import transaction
from flight.models import Airline, Location, Flight, Stopover, Ticket

fake = Faker()

class Command(BaseCommand):
    help = 'Generate random flight data'

    def add_arguments(self, parser):
        parser.add_argument('num_flights', type=int, help='Number of flights to generate')

    @transaction.atomic
    def handle(self, *args, **kwargs):
        num_flights = kwargs['num_flights']
        for _ in range(num_flights):
            self.generate_random_flight()

        self.stdout.write(self.style.SUCCESS(f'{num_flights} flights generated successfully'))

def generate_random_flight(self):
    airline = Airline.objects.order_by('?').first()
    departure_location = Location.objects.order_by('?').first()
    arrival_location = Location.objects.exclude(id=departure_location.id).order_by('?').first()
    
    # Set departure date within the specified range
    start_date = datetime.datetime(2024, 5, 16)
    end_date = datetime.datetime(2024, 12, 16)
    departure_datetime = fake.date_time_between_dates(start_date=start_date, end_date=end_date)
    
    flight_duration = datetime.timedelta(hours=random.randint(1, 24), minutes=random.randint(0, 59))
    base_price = round(random.uniform(50, 1000), 2)
    passenger_type = random.choice(['Adult', 'Minor'])
    flight_class = random.choice(['Business', 'Economic'])
    checked_bag_price = round(random.uniform(0, 50), 2)
    
    # Determine number of flights for the day based on passenger type and flight class
    if passenger_type == 'Adult':
        num_flights_today = random.randint(5, 10)
    else:
        num_flights_today = random.randint(5, 10)
    
    if flight_class == 'Business':
        num_flights_today = random.randint(5, 10)
    else:
        num_flights_today = random.randint(5, 10)
    
    for _ in range(num_flights_today):
        flight = Flight.objects.create(
            airline=airline,
            departure_location=departure_location,
            arrival_location=arrival_location,
            departure_datetime=departure_datetime,
            flight_duration=flight_duration,
            base_price=base_price,
            passenger_type=passenger_type,
            flight_class=flight_class,
            checked_bag_price=checked_bag_price
        )

        # Generate stopovers randomly
        if random.choice([True, False]):
            num_stopovers = random.randint(1, 3)
            for _ in range(num_stopovers):
                stopover_location = Location.objects.exclude(id__in=[departure_location.id, arrival_location.id]).order_by('?').first()
                duration = datetime.timedelta(hours=random.randint(1, 12), minutes=random.randint(0, 59))
                Stopover.objects.create(flight=flight, location=stopover_location, duration=duration)

        # Generate tickets
        num_tickets = random.randint(50, 300)
        for _ in range(num_tickets):
            Ticket.objects.create(flight=flight)
