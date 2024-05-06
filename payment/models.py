from django.db import models
from booking.models import Booking
from account.models import User
from base.models import BaseModel

class Payment(BaseModel):
    SUCCESS = 'success'
    FAILED = 'failed'
    PENDING = 'pending'
    
    PAYMENT_STATUS_CHOICES = (
        (SUCCESS, 'Success'),
        (FAILED, 'Failed'),
        (PENDING, 'Pending'),
    )

    booking_id = models.ForeignKey(Booking, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=50)
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default=PENDING)
    payment_intent_id = models.CharField(max_length=100, blank=True, null=True)
    payment_method_id = models.CharField(max_length=100, blank=True, null=True)
    card_token = models.CharField(max_length=150, blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.booking} - {self.payment_status}"