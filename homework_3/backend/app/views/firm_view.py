from rest_framework import generics
from ..models import Firm
from ..serializer import FirmSerializer

# View for retrieving all firms
class FirmView(generics.ListAPIView):
    queryset = Firm.objects.all()
    serializer_class = FirmSerializer


class FirmDetailView(generics.RetrieveAPIView):
    queryset = Firm.objects.all()
    serializer_class = FirmSerializer
    lookup_field = 'firm_id'
