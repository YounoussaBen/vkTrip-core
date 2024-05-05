# urls.py
from django.urls import path
from .views import PassengerListCreateAPIView, PassengerRetrieveUpdateDestroyAPIView

urlpatterns = [
    path('', PassengerListCreateAPIView.as_view(), name='flight-list-create'),
    path('<uuid:pk>/', PassengerRetrieveUpdateDestroyAPIView.as_view(), name='flight-retrieve-update-destroy'),
]
