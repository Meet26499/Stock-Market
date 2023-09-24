from django.db import models
from ..models import Company

class Inventory(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0, null=True, blank=True)
    avg_buy_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
