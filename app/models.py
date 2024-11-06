from django.db import models

class Firm(models.Model):
    firm_id = models.IntegerField(max_length=10, unique=True)
    firm_name = models.CharField(max_length=30)

    class Meta:
        db_table = 'firms'

class Share(models.Model):
    firm_id = models.ForeignKey(Firm, on_delete=models.CASCADE, to_field="firm_id")
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

class User(models.Model):
    first_name = models.CharField(max_length=15)
    last_name = models.CharField(max_length=25)
    username = models.CharField(max_length=30)
    email = models.CharField(max_length=50)
    password = models.CharField(max_length=128)
    date_joined = models.DateField()

    class Meta:
        db_table = 'users'

class Transaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, to_field="username")
    share = models.ForeignKey(Share, on_delete=models.CASCADE, to_field="firm_id")
    date = models.DateField()
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    quantity_of_shares = models.IntegerField(default=0)
    total_profit = models.DecimalField(max_digits=15, decimal_places=2, default=0)

    class Meta:
        db_table = 'transactions'

class MyStocks(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, to_field="username")
    share = models.ForeignKey(Share, on_delete=models.CASCADE, to_field="firm_id")
    quantity_of_shares = models.IntegerField(default=0)
    purchase_date = models.DateField()

    class Meta:
        db_table = 'my_stocks'