from rest_framework import generics
from app.models import Firm
from app.serializer import FirmSerializer

class FirmView(generics.ListCreateAPIView):
    queryset = Firm.objects.all()
    serializer_class = FirmSerializer