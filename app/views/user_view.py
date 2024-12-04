from rest_framework import generics
from app.models import User
from app.serializer import UserSerializer

class UserView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer