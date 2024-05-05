# urls.py
from django.urls import path
from .views import FlightListCreateAPIView, FlightRetrieveUpdateDestroyAPIView

urlpatterns = [
    path('list-create/', FlightListCreateAPIView.as_view(), name='flight-list-create'),
    path('<int:pk>/', FlightRetrieveUpdateDestroyAPIView.as_view(), name='flight-retrieve-update-destroy'),
]
