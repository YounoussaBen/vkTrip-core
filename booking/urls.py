from .views import BookingListCreateView, BookingRetrieveUpdateDestroyView
from django.urls import path

urlpatterns = [
    path('list-create/', BookingListCreateView.as_view(), name='booking-list-create'),
    path('<int:pk>/', BookingRetrieveUpdateDestroyView.as_view(), name='booking-retrieve-update-destroy'),
]