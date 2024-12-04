from django.db import models

class TransactionShare(models.Model):
    TRANSACTION_TYPE_CHOICES = [
        ('BUY', 'Buy'),
        ('SELL', 'Sell'),
    ]
    user = models.ForeignKey("app.User", on_delete=models.CASCADE, related_name='transactions_shares')
    firm = models.ForeignKey("app.Firm", on_delete=models.CASCADE)
    transaction_type = models.CharField(max_length=4, choices=TRANSACTION_TYPE_CHOICES)
    quantity = models.IntegerField()
    transaction_date = models.DateTimeField(auto_now_add=True)
    price = models.DecimalField(max_digits=15, decimal_places=2)

    class Meta:
        db_table = 'transactions_shares'