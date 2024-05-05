# Generated by Django 5.0.4 on 2024-05-05 02:28

import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("flight", "0002_alter_flight_arrival_datetime_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="flight",
            name="flight_class",
        ),
        migrations.CreateModel(
            name="Ticket",
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
                ("is_booked", models.BooleanField(default=False)),
                (
                    "flight",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="tickets",
                        to="flight.flight",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
    ]