from django.urls import path
from .view import (SignupView, LoginView, RefreshTokenView)

urlpatterns = [
    # AUTH ENDPOINTS
    path('signup/', SignupView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('login/refresh/', RefreshTokenView.as_view(), name='refresh-token'),
]