from rest_framework import generics
from ..models import Firm
from ..serializer import FirmSerializer

class FirmView(generics.ListCreateAPIView):
    queryset = Firm.objects.all()
    serializer_class = FirmSerializer