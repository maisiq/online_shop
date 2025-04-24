from django.contrib import admin

from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 3

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['order', 'product', 'amount', 'price']

@admin.register(Order)
class OrderLineAdmin(admin.ModelAdmin):
    list_display = ['customer']
    list_select_related = ['customer']

    inlines = [OrderItemInline]

