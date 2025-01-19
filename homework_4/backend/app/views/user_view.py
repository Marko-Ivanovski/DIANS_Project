from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError
from decimal import Decimal
from ..models import User
from ..serializer import UserSerializer

class UserView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserFirstNameView(APIView):
    def get(self, request):
        user = request.user
        return Response({"first_name": user.first_name})

class UserDetailView(APIView):
    permission_classes = [IsAuthenticated]  # Ensure JWT authentication is required

    def get(self, request):
        """Fetch user's details."""
        user = request.user
        return Response({
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email,
            "balance": user.current_balance,
        })

    def put(self, request):
        """Update user's personal details."""
        user = request.user
        data = request.data

        # Update user fields
        user.first_name = data.get("first_name", user.first_name)
        user.last_name = data.get("last_name", user.last_name)
        user.email = data.get("email", user.email)

        if "password" in data:
            user.set_password(data["password"])  # Hash password securely

        user.save()
        return Response({"message": "User details updated successfully!"})

    def post(self, request):
        """Add balance to the user's account."""
        amount = request.data.get("amount")

        if not amount:
            raise ValidationError({"amount": "This field is required."})

        try:
            amount = Decimal(amount)
        except (ValueError, TypeError):
            raise ValidationError({"amount": "Invalid decimal amount."})

        if amount <= 0:
            raise ValidationError({"amount": "Amount must be greater than zero."})

        # Update user's balance
        user = request.user
        user.current_balance += amount
        user.save()

        return Response({"message": "Balance added successfully!", "new_balance": user.current_balance})