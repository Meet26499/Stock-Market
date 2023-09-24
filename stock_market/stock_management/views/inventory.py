from rest_framework import generics
from ..models import Inventory, Transaction
from ..serializers import InventorySerializer
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from datetime import datetime


class InventoryListView(generics.ListAPIView):
    queryset = Inventory.objects.all()
    serializer_class = InventorySerializer

class AverageBuyPriceView(generics.RetrieveAPIView):
    serializer_class = InventorySerializer

    def get_object(self):
        company_id = self.request.query_params.get('company_id', None)
        date = self.request.query_params.get('date', None)

        if not company_id or not date:
            return None

        # Convert date string to a datetime object
        try:
            date = datetime.strptime(date, '%d/%m/%Y').date()
        except ValueError:
            return None

        # Retrieve the inventory for the specified company up to the given date
        inventory = get_object_or_404(Inventory, company_id=company_id)
        buy_transactions = Transaction.objects.filter(
            company_id=company_id,
            trading_type='BUY',
            trading_date__lte=date
        ).order_by('trading_date')

        total_quantity = 0
        total_cost = 0

        for transaction in buy_transactions:
            total_quantity += transaction.quantity
            total_cost += transaction.quantity * transaction.price

        if total_quantity == 0:
            return None

        avg_buy_price = total_cost / total_quantity
        inventory.avg_buy_price = avg_buy_price
        inventory.quantity = total_quantity

        return inventory