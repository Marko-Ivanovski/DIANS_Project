from rest_framework import generics
from app.models import TransactionShare
from app.serializer import TransactionShareSerializer

class TransactionSharesView(generics.ListCreateAPIView):
    queryset = TransactionShare.objects.all()
    serializer_class = TransactionShareSerializer