from rest_framework import serializers
from ..models import Transaction

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = '__all__'

class TransactionSplitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ['trading_type', 'split_ratio']