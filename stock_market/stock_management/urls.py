# stock_market/urls.py

from django.urls import path
from .views import TransactionCreateView, InventoryListView, AverageBuyPriceView

urlpatterns = [
    path('transactions/', TransactionCreateView.as_view(), name='transaction-create'),
    path('inventory/', InventoryListView.as_view(), name='inventory-list'),
    path('average_buy_price/', AverageBuyPriceView.as_view(), name='average-buy-price'),
]
