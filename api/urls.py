from django.urls import include, path

urlpatterns = [
    path("auth/", include("authentication.urls")),
    path("account/", include("account.urls")),
    path("flight/", include("flight.urls")),
    path("passenger/", include("passenger.urls")),
    path("booking/", include("booking.urls")),
    path("payment/", include("payment.urls")),
]
