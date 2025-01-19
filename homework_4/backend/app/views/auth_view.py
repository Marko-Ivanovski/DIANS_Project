from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from django.http import JsonResponse
from ..service.auth_service import signup_user
import json

class SignupView(APIView):
    def post(self, request):
        try:
            data = json.loads(request.body)
            first_name = data.get('first_name')
            last_name = data.get('last_name')
            email = data.get('email')
            password = data.get('password')

            user = signup_user(first_name, last_name, email, password)
            return JsonResponse({"message": "User created successfully", "user_id": user.id}, status=201)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)


class LoginView(APIView):
    def post(self, request):
        try:
            data = json.loads(request.body)
            email = data.get('email')
            password = data.get('password')

            user = authenticate(username=email, password=password)
            if user is None:
                return JsonResponse({"error": "Invalid email or password."}, status=400)

            # Generate JWT tokens
            refresh = RefreshToken.for_user(user)
            access_token = refresh.access_token

            return JsonResponse({
                "message": "Login successful",
                "user_id": user.id,
                "access_token": str(access_token),
                "refresh_token": str(refresh),
            }, status=200)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

class RefreshTokenView(APIView):
    def post(self, request):
        try:
            data = json.loads(request.body)
            refresh_token = data.get("refresh_token")

            # Validate the refresh token
            refresh = RefreshToken(refresh_token)
            new_access_token = refresh.access_token

            return JsonResponse({
                "message": "Token refreshed successfully",
                "access_token": str(new_access_token),
            }, status=200)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)