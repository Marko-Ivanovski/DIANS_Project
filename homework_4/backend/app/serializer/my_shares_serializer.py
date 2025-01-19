from rest_framework import serializers
from ..models import MyShares

class MySharesSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyShares
        fields = ['id', 'share', 'firm', 'quantity', 'price_of_last_transaction', 'purchase_date']
