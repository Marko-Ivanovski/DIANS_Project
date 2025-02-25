from rest_framework import serializers
from ..models import TransactionLog

class TransactionLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransactionLog
        fields = ['user', 'transaction_account_type', 'amount']