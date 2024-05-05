from django.urls import path
from .views import PaymentAPI

urlpatterns = [
    path('visa-card', PaymentAPI.as_view(), name='visa_card_payment')
]