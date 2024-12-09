from django.db import models

class Firm(models.Model):
    firm_id = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=30, blank=True)

    class Meta:
        db_table = 'firms'