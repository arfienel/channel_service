from django.db import models


class Order(models.Model):
    id = models.IntegerField(primary_key=True)
    order_number = models.CharField(max_length=50, unique=True)
    cost_usd = models.IntegerField()
    cost_rub = models.FloatField()
    supply_date = models.DateField()
