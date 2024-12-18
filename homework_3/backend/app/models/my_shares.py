from django.db import models

class MyShares(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE, related_name='my_shares')
    firm = models.ForeignKey("Firm", on_delete=models.CASCADE, to_field="firm_id", null=False)
    share = models.OneToOneField('Share', on_delete=models.CASCADE)
    quantity = models.IntegerField() 
    price_of_last_transaction = models.DecimalField(max_digits=15, decimal_places=2)
    purchase_date = models.DateField(auto_now_add=True)

    class Meta:
        db_table = 'my_shares'
