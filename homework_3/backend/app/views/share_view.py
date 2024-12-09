from rest_framework import generics
from ..models import Share
from ..serializer import ShareSerializer

class ShareView(generics.ListAPIView):
    queryset = Share.objects.all()
    serializer_class = ShareSerializer