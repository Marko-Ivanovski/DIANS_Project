from rest_framework import generics
from ..models import TransactionLog
from ..serializer import TransactionLogSerializer

class TransactionLogsView(generics.ListAPIView):
    queryset = TransactionLog.objects.all()
    serializer_class = TransactionLogSerializer