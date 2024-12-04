from django.db import models

class User(models.Model):
    first_name = models.CharField(max_length=15)
    last_name = models.CharField(max_length=50)
    username = models.CharField(max_length=30, unique=True)
    email = models.EmailField(unique=True)
    current_balance = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    password = models.CharField(max_length=8000)  # Note: Store hashed passwords!
    date_joined = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'users'