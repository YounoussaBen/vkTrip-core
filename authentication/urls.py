from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.urls import path, include

urlpatterns = [
    path("get-token/", TokenObtainPairView.as_view(), name="get_token"),
    path("refresh-token/", TokenRefreshView.as_view(), name="refresh_token"),
    # path("social-login/", include("drf_social_oauth2.urls", namespace="social_login")),
]