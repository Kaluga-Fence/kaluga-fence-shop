from django.contrib import admin
from .models import Product, Order

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'size', 'price', 'available')
    list_filter = ('category', 'available')
    list_editable = ('available',)

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'address', 'created_at', 'status')
    list_filter = ('status', 'created_at')
