from django.core.management.base import BaseCommand
from flight.models import Airline

class Command(BaseCommand):
    help = 'Create airlines'

    airlines_data = [
        {"name": "Hawaiian Airline"},
        {"name": "Delta Airline"},
        {"name": "Korean Air"},
        {"name": "Air France"},
        {"name": "Qantas Airline"},
        {"name": "Emirates"},
        {"name": "Air China"},
        {"name": "United Airline"},
        {"name": "Japon Airline"},
        {"name": "Eva Air"}
    ]

    def handle(self, *args, **kwargs):
        for data in self.airlines_data:
            Airline.objects.create(name=data["name"])

        self.stdout.write(self.style.SUCCESS('Airlines created successfully'))