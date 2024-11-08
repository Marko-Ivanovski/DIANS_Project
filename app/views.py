from rest_framework import viewsets
from .models import Firm, Share
from .serializers import FirmSerializer, ShareSerializer

class FirmViewSet(viewsets.ModelViewSet):
    queryset = Firm.objects.all()
    serializer_class = FirmSerializer

class ShareViewSet(viewsets.ModelViewSet):
    queryset = Share.objects.all()
    serializer_class = ShareSerializer
