from django.contrib import admin
from .models import Order, OrderItem


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['user', 'status']
    list_filter = ['status']

@admin.register(OrderAdmin)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['order', 'product', 'ammount']
    list_filter = ['product']
