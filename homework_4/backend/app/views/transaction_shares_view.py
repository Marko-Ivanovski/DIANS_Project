from rest_framework import generics
from ..models import TransactionShare
from ..serializer import TransactionShareSerializer

class TransactionSharesView(generics.ListCreateAPIView):
    queryset = TransactionShare.objects.all()
    serializer_class = TransactionShareSerializer