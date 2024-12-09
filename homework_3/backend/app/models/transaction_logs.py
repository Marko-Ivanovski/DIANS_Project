from django.db import models

class TransactionLog(models.Model):
    TRANSACTION_ACCOUNT_TYPE_CHOICES = [
        ('DEPOSIT', 'Deposit'),
        ('WITHDRAW', 'Withdraw'),
    ]
    user = models.ForeignKey("User", on_delete=models.CASCADE, related_name='transactions_logs')
    transaction_account_type = models.CharField(max_length=20, choices=TRANSACTION_ACCOUNT_TYPE_CHOICES)
    amount = models.DecimalField(max_digits=15, decimal_places=2)

    class Meta:
        db_table = 'transactions_logs'