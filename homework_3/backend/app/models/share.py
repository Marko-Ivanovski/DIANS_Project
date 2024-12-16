from django.db import models

class Share(models.Model):
    firm = models.ForeignKey("Firm", on_delete=models.CASCADE, related_name='shares', to_field="firm_id", null=False)
    date = models.DateField()
    price_of_last_transaction = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    max_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    min_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    average_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    percent_changed = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    quantity_of_shares = models.IntegerField(default=0)
    total_profit = models.DecimalField(max_digits=15, decimal_places=2, default=0)

    class Meta:
        db_table = 'shares'