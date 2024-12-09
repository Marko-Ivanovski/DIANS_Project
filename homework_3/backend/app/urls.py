from django.urls import path
from .views import (FirmView, ShareView, UserView, TransactionSharesView, TransactionLogsView)

urlpatterns = [
    path('firms/', FirmView.as_view(), name='firm-list'),
    path('shares/', ShareView.as_view(), name='share-list'),
    path('users/', UserView.as_view(), name='user-list'),
    path('transactions/shares/', TransactionSharesView.as_view(), name='transaction-shares-list'),
    path('transactions/logs/', TransactionLogsView.as_view(), name='transaction-logs-list'),
]