# import_airports.py

import csv
from django.core.management.base import BaseCommand
from flight.models import Location 

class Command(BaseCommand):
    help = 'Import airport data from a CSV file'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='Path to the CSV file')

    def handle(self, *args, **kwargs):
        csv_file = kwargs['csv_file']
        with open(csv_file, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                airport_name = row['name']
                country = row['country']
                # Create Location object
                location = Location(airport_name=airport_name, country=country)
                location.save()
        self.stdout.write(self.style.SUCCESS('Airport data imported successfully'))
