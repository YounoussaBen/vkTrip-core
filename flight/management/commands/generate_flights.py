import random
import datetime
from faker import Faker
from django.core.management.base import BaseCommand
from django.db import transaction
from flight.models import Airline, Location, Flight, Stopover, Ticket

fake = Faker()

class Command(BaseCommand):
    help = 'Generate random flight data'

    @transaction.atomic
    def handle(self, *args, **kwargs):
        start_date = datetime.date.today()
        end_date = start_date + datetime.timedelta(days=30)  # Generate flights for a month

        while start_date < end_date:
            self.generate_random_flights_for_day(start_date)
            start_date += datetime.timedelta(days=1)

        self.stdout.write(self.style.SUCCESS('Flights generated successfully for the month'))

    def generate_random_flights_for_day(self, date):
        num_flights = random.randint(3, 5)  # Generate 3-5 flights per day

        for _ in range(num_flights):
            self.generate_random_flight(date)

    def generate_random_flight(self, date):
        airline = Airline.objects.order_by('?').first()
        departure_location = Location.objects.order_by('?').first()
        arrival_location = Location.objects.exclude(id=departure_location.id).order_by('?').first()
        departure_datetime = fake.date_time_between_dates(datetime_start=date, datetime_end=date, tzinfo=None, delta_start="-1y", delta_end="+1y")
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
