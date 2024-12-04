from rest_framework import serializers
from app.models import Firm

class FirmSerializer(serializers.ModelSerializer):
    class Meta:
        model = Firm
        fields = ['firm_id', 'name']