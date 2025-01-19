from rest_framework import serializers
from ..models import Share

class ShareSerializer(serializers.ModelSerializer):
    class Meta:
        model = Share
        fields = ['id','firm', 'date', 'price_of_last_transaction', 'max_price', 'min_price', 'average_price', 'percent_changed', 'quantity_of_shares', 'total_profit']