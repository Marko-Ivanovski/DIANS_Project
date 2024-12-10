from django.http import JsonResponse
from django.views import View
from ..service.auth_service import signup_user, login_user
import json

class SignupView(View):
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


class LoginView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            email = data.get('email')
            password = data.get('password')

            user = login_user(email, password)
            return JsonResponse({"message": "Login successful", "user_id": user.id}, status=200)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)