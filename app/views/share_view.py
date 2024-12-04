from rest_framework import generics
from app.models import Share
from app.serializer import ShareSerializer

class ShareView(generics.ListAPIView):
    queryset = Share.objects.all()
    serializer_class = ShareSerializer