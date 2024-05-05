# urls.py
from django.urls import path
from .views import FlightListCreateAPIView, FlightRetrieveUpdateDestroyAPIView, LocationListAPIView, RoundTripFlightSearchAPIView, FlightSearchAPIView

urlpatterns = [
    path('', FlightListCreateAPIView.as_view(), name='flight-list-create'),
    path('<int:pk>/', FlightRetrieveUpdateDestroyAPIView.as_view(), name='flight-retrieve-update-destroy'),
    path('locations/', LocationListAPIView.as_view(), name='location-list'),
    path('round-trip-search/', RoundTripFlightSearchAPIView.as_view(), name='round-trip-search'),
    path('one-way-search/', FlightSearchAPIView.as_view(), name='flight-search'),
]
