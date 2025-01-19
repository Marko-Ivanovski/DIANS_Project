from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from django.http import JsonResponse
from .service import signup_user
import logging

logger = logging.getLogger(__name__)  # Configure logging

class SignupView(APIView):
    """
    Handles user signup by creating a new user and returning a success message.
    """
    permission_classes = [AllowAny]

    def post(self, request):
        try:
            data = request.data  # DRF parses JSON automatically
            first_name = data.get('first_name')
            last_name = data.get('last_name')
            email = data.get('email')
            password = data.get('password')

            user = signup_user(first_name, last_name, email, password)
            return Response({"message": "User created successfully", "user_id": user.id}, status=201)
        except Exception as e:
            logger.error(f"Signup error: {e}")
            return Response({"error": "Unable to create user. Please try again."}, status=400)


class LoginView(APIView):
    """
    Handles user login by validating credentials and returning JWT tokens.
    """
    permission_classes = [AllowAny]

    def post(self, request):
        try:
            data = request.data
            email = data.get('email')
            password = data.get('password')

            # Authenticate user
            user = authenticate(request, username=email, password=password)
            if user is None:
                raise AuthenticationFailed("Invalid email or password.")

            # Generate tokens
            refresh = RefreshToken.for_user(user)
            access_token = refresh.access_token

            # Set tokens as HTTP-only cookies
            response = JsonResponse({
                "message": "Login successful",
                "user_id": user.id,
            }, status=200)
            response.set_cookie("access_token", str(access_token), httponly=True, secure=True)
            response.set_cookie("refresh_token", str(refresh), httponly=True, secure=True)
            return response
        except AuthenticationFailed as e:
            return Response({"error": str(e)}, status=401)
        except Exception as e:
            logger.error(f"Login error: {e}")
            return Response({"error": "Unable to log in. Please try again."}, status=400)


class RefreshTokenView(APIView):
    """
    Refreshes the access token using a valid refresh token.
    """
    permission_classes = [AllowAny]

    def post(self, request):
        try:
            refresh_token = request.COOKIES.get("refresh_token")  # Get token from cookies

            if not refresh_token:
                raise AuthenticationFailed("Refresh token not provided.")

            # Validate and generate new access token
            refresh = RefreshToken(refresh_token)
            new_access_token = refresh.access_token

            # Return new access token as a cookie
            response = JsonResponse({
                "message": "Token refreshed successfully",
            }, status=200)
            response.set_cookie("access_token", str(new_access_token), httponly=True, secure=True)
            return response
        except AuthenticationFailed as e:
            return Response({"error": str(e)}, status=401)
        except Exception as e:
            logger.error(f"Token refresh error: {e}")
            return Response({"error": "Unable to refresh token. Please log in again."}, status=400)
