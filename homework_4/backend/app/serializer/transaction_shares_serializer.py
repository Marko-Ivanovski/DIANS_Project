from rest_framework import serializers
from ..models import TransactionShare

class TransactionShareSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransactionShare
        fields = ['user', 'firm', 'transaction_type', 'quantity', 'transaction_date', 'price']