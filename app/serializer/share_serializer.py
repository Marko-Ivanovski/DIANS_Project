from rest_framework import serializers
from app.models import Share

class ShareSerializer(serializers.ModelSerializer):
    class Meta:
        model = Share
        fields = ['firm', 'date', 'price_of_last_transaction', 'max_price', 'min_price', 'average_price', 'percent_changed', 'quantity_of_shares', 'total_profit']