#!/usr/bin/env bash

set -o errexit  # Exit on error

# Upgrade pip to the latest version
pip install --upgrade pip

# Set DJANGO_SETTINGS_MODULE to settings.production
export DJANGO_SETTINGS_MODULE=settings.prod

# Install the required packages
pip install -r requirements.txt

# Collect static files
python manage.py collectstatic --no-input

# Apply database migrations
python manage.py migrate

# Create superuser if applicable
python manage.py createsu

# Import Airports
python manage.py import_airports data/airports_by_country.csv

#Create Airlines
python manage.py create_airlines

# Populate flight
python manage.py generate_flights 10000
