# Generated by Django 3.2.17 on 2024-05-06 06:47

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('booking', '0002_booking_status'),
    ]

    operations = [
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('is_deleted', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('total_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('payment_method', models.CharField(max_length=50)),
                ('payment_status', models.CharField(choices=[('success', 'Success'), ('failed', 'Failed'), ('pending', 'Pending')], default='pending', max_length=20)),
                ('payment_intent_id', models.CharField(blank=True, max_length=100, null=True)),
                ('payment_method_id', models.CharField(blank=True, max_length=100, null=True)),
                ('card_token', models.CharField(blank=True, max_length=150, null=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('booking_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='booking.booking')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
