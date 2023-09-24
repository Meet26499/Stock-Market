from django.contrib import admin
from .models import Transaction, Company, Inventory

# Register your models here., 
@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ['company', 'trading_type', 'quantity', 'price']

@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ['name']

@admin.register(Inventory)
class InventoryAdmin(admin.ModelAdmin):
    list_display = ['company', 'quantity']