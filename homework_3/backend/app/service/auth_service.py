from ..models import User
from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError


def signup_user(first_name: str, last_name: str, email: str, password: str):
    if User.objects.filter(email=email).exists():
        raise ValidationError("Email is already taken.")

    user = User.objects.create_user(
        username=email,
        first_name=first_name,
        last_name=last_name,
        email=email,
        password=password,
    )
    return user


def login_user(email: str, password: str):
    user = authenticate(username=email, password=password)
    if user is None:
        raise ValidationError("Invalid email or password.")
    return user