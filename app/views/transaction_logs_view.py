from rest_framework import generics
from app.models import TransactionLog
from app.serializer import TransactionLogSerializer

class TransactionLogsView(generics.ListAPIView):
    queryset = TransactionLog.objects.all()
    serializer_class = TransactionLogSerializer