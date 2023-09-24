from rest_framework import generics
from ..models import Transaction, Inventory
from ..serializers import TransactionSerializer, TransactionSplitSerializer
from rest_framework.response import Response
from rest_framework import status
from datetime import datetime

class TransactionCreateView(generics.CreateAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        self.update_inventory(serializer.validated_data)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update_inventory(self, transaction):
        if transaction.get('trading_type') == 'BUY':
            self.update_inventory_buy(transaction)
        elif transaction.get('trading_type') == 'SELL':
            self.update_inventory_sell(transaction)
        elif transaction.get('trading_type') == 'SPLIT':
            self.update_inventory_split(transaction)

    def update_inventory_buy(self, transaction):
        # Update inventory for BUY transactions
        inventory, created = Inventory.objects.get_or_create(company=transaction.get('company'))
        if created:
            # If inventory for this company doesn't exist, initialize it
            inventory.avg_buy_price = transaction.get('price')
            inventory.quantity = transaction.get('quantity')
        else:
            # Update average buy price and quantity
            old_avg_buy_price = inventory.avg_buy_price
            old_quantity = inventory.quantity
            new_quantity = old_quantity + transaction.get('quantity')
            new_avg_buy_price = ((old_avg_buy_price * old_quantity) + (transaction.get('price') * transaction.get('quantity'))) / new_quantity
            inventory.avg_buy_price = new_avg_buy_price
            inventory.quantity = new_quantity
        inventory.save()

    def update_inventory_sell(self, transaction):
        remaining_quantity_to_sell = transaction.get('quantity')
        buy_transactions = Transaction.objects.filter(
            company=transaction.get('company'),
            trading_type='BUY',
            quantity__gt=0,
            trading_date__lte=datetime.now()
        ).order_by('trading_date')

        qty_x_price = 0
        for buy_transaction in buy_transactions:
            print(remaining_quantity_to_sell, "remaining_quantity_to_sell   ")

            # Calculate how many shares from this buy order should be used
            shares_to_use = min(buy_transaction.quantity, remaining_quantity_to_sell)

            # Update the buy order quantity
            buy_transaction.quantity -= shares_to_use
            buy_transaction.save()

            remaining_quantity_to_sell -= shares_to_use

            qty_x_price += buy_transaction.quantity * buy_transaction.price
            print(qty_x_price, "qty_x_price")
            print(buy_transaction.quantity, "buy_transaction")
            print(buy_transaction.price, "buy_transaction")

        # Update the inventory based on the adjusted buy orders
        inventory, created = Inventory.objects.get_or_create(company=transaction.get('company'))
        if created:
            raise Exception("Inventory should have been created for this company for selling.")

        inventory.quantity -= transaction.get('quantity')
        inventory.avg_buy_price = qty_x_price / inventory.quantity
        inventory.save()

    def update_inventory_split(self, transaction):
        buy_transactions = Transaction.objects.filter(
            company=transaction.get('company'),
            trading_type='BUY',
            trading_date__lte=datetime.now()
        )

        split_ratio = transaction.get('split_ratio')
        if not split_ratio:
            raise ValueError("Split ratio is required for a SPLIT transaction.")

        # Split ratio format: "1:5"
        split_ratio_parts = split_ratio.split(":")
        if len(split_ratio_parts) != 2:
            raise ValueError("Invalid split ratio format. Use 'x:y' format.")

        try:
            old_ratio, new_ratio = int(split_ratio_parts[0]), int(split_ratio_parts[1])
            inventory, created = Inventory.objects.get_or_create(company=transaction.get('company'))
            if created:
                raise Exception("Inventory should have been created for this company for the split.")

            # Adjust the quantity and average buy price based on the split ratio
            inventory.quantity *= new_ratio
            inventory.avg_buy_price /= new_ratio

            inventory.save()

            for buy_transaction in buy_transactions:
                buy_transaction.quantity *= new_ratio
                buy_transaction.price /= new_ratio
                buy_transaction.save()

        except ValueError:
            raise ValueError("Split ratio parts must be integers.")
        
