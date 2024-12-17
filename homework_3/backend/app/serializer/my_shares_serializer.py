from rest_framework import serializers
from ..models import MyShares

class MySharesSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyShares
        fields = ['id', 'firm', 'quantity', 'last_purchase_price', 'purchase_date']
