from django.contrib import admin

from .models import Delivery


@admin.register(Delivery)
class DeliveryAdmin(admin.ModelAdmin):
    list_display = ['type', 'address', 'receiver', 'customer']
    list_select_related = ['customer']
