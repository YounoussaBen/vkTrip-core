# Generated by Django 5.0.4 on 2024-05-05 12:56

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("booking", "0002_booking_completed"),
    ]

    operations = [
        migrations.AddField(
            model_name="booking",
            name="checked_bags",
            field=models.PositiveIntegerField(default=0),
        ),
    ]