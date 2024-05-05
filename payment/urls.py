from django.urls import path
from .views import PaymentAPI

urlpatterns = [
    path('stripe', PaymentAPI.as_view(), name='stripe_payment')
]