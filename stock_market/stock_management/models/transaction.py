from django.db import models
from ..models import Company

class Transaction(models.Model):
    TRANSACTION_TYPES = (
        ('BUY', 'Buy'),
        ('SELL', 'Sell'),
        ('SPLIT', 'Split'),
    )
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    trading_date = models.DateField(auto_now_add=True)
    trading_type = models.CharField(max_length=10, choices=TRANSACTION_TYPES)
    quantity = models.PositiveIntegerField(default=0, null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, help_text="Price Per Share")
    split_ratio = models.CharField(max_length=10, blank=True, null=True)

