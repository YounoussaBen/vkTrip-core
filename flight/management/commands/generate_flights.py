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
        parser.add_argument('start_date', type=str, help='Start date (YYYY-MM-DD)')
        parser.add_argument('num_days', type=int, help='Number of days to generate flights')

    @transaction.atomic
    def handle(self, *args, **kwargs):
        start_date = datetime.datetime.strptime(kwargs['start_date'], '%Y-%m-%d')
        num_days = kwargs['num_days']
        end_date = start_date + datetime.timedelta(days=num_days)

        while start_date < end_date:
            num_flights = random.randint(3, 5)
            for _ in range(num_flights):
                self.generate_random_flight(start_date, duplicates=3)
            start_date += datetime.timedelta(days=1)

        self.stdout.write(self.style.SUCCESS(f'Flights generated successfully'))

    def generate_random_flight(self, date, duplicates=3):
        for _ in range(duplicates):
            airline = Airline.objects.order_by('?').first()
            departure_location = Location.objects.order_by('?').first()
            arrival_location = Location.objects.exclude(id=departure_location.id).order_by('?').first()
            departure_datetime = datetime.datetime.combine(date, fake.time_object())
            flight_duration = datetime.timedelta(hours=random.randint(1, 24), minutes=random.randint(0, 59))
            base_price = round(random.uniform(50, 1000), 2)
            passenger_type = random.choice(['Adult', 'Minor'])
            flight_class = random.choice(['Business', 'Economic'])
            checked_bag_price = round(random.uniform(0, 50), 2)
            num_tickets = random.randint(50, 300)

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
            for _ in range(num_tickets):
                Ticket.objects.create(flight=flight)
