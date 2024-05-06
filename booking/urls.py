from .views import BookingListCreateView, BookingRetrieveUpdateDestroyView
from django.urls import path

urlpatterns = [
    path('', BookingListCreateView.as_view(), name='booking-list-create'),
    path('<uuid:pk>/', BookingRetrieveUpdateDestroyView.as_view(), name='booking-retrieve-update-destroy'),
]