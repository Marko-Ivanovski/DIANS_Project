from rest_framework import serializers
from .models import Firm, Share

class FirmSerializer(serializers.ModelSerializer):
    class Meta:
        model = Firm
        fields = ['firm_id', 'name']

class ShareSerializer(serializers.ModelSerializer):
    firm = FirmSerializer()  # Nested serializer for Firm

    class Meta:
        model = Share
        fields = ['firm', 'date', 'price_of_last_transaction', 'max_price', 'min_price',
                  'average_price', 'percent_changed', 'quantity_of_shares', 'total_profit']
