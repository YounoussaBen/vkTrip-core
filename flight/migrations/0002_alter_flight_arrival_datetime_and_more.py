# Generated by Django 5.0.4 on 2024-05-05 01:42

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("flight", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="flight",
            name="arrival_datetime",
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="flight",
            name="arrival_location",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="arrivals",
                to="flight.location",
            ),
        ),
    ]
