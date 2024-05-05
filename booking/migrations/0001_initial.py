# Generated by Django 5.0.4 on 2024-05-05 02:49

import django.db.models.deletion
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("flight", "0004_rename_arrival_datetime_flight_return_datetime"),
        ("passenger", "0002_emergencycontact_passenger_passportexpiration_and_more"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Booking",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("is_deleted", models.BooleanField(default=False)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "trip_type",
                    models.CharField(
                        choices=[("Round Trip", "Round Trip"), ("One Way", "One Way")],
                        max_length=20,
                    ),
                ),
                (
                    "flight_class",
                    models.CharField(
                        choices=[
                            ("Business", "Business Class"),
                            ("Economic", "Economic Class"),
                        ],
                        max_length=20,
                    ),
                ),
                ("total_price", models.DecimalField(decimal_places=2, max_digits=10)),
                (
                    "created_by",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "flights",
                    models.ManyToManyField(related_name="bookings", to="flight.flight"),
                ),
                (
                    "passengers",
                    models.ManyToManyField(
                        related_name="bookings", to="passenger.passenger"
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
    ]