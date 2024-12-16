from django.urls import path
from .views import (FirmView, FirmDetailView, ShareView, ShareByFirmView, SharesFilteredView, UserView, UserDetailView,
                    TransactionSharesView, TransactionLogsView, SignupView, LoginView, RefreshTokenView)

urlpatterns = [
    path('users/', UserView.as_view(), name='user-list'),
    path('transactions/shares/', TransactionSharesView.as_view(), name='transaction-shares-list'),
    path('transactions/logs/', TransactionLogsView.as_view(), name='transaction-logs-list'),

    # HOME PAGE GRAPH
    path('firms/', FirmView.as_view(), name='firm-list'),
    path('firms/<str:firm_id>/', FirmDetailView.as_view(), name='firm-shares-list'),
    path('shares/', ShareView.as_view(), name='share-list'),
    path('shares/<str:firm_id>/', ShareByFirmView.as_view(), name='share-by-firm-list'),
    path('shares/average-price', SharesFilteredView.as_view(), name='share-average-price'),

    # AUTH ENDPOINTS
    path('signup/', SignupView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('login/refresh/', RefreshTokenView.as_view(), name='refresh-token'),
    path('edit-user/', UserDetailView.as_view(), name="user-detail"),
]