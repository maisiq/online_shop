import datetime as dt
import random
import string

from django.db import models
from uuid_extensions import uuid7


class Order(models.Model):
    class OrderStatus(models.TextChoices):
        PROCESS = 'ordered'  # Обрабатываем и собираем заказ
        DELIVERY = 'delivery'  # Отдан в доставку
        READY = 'ready'  # Готов к получению
        RECEIVED = 'received'  # Получен

    id = models.UUIDField(primary_key=True, default=uuid7, editable=False)
    paid = models.BooleanField(default=False)
    customer = models.ForeignKey('users.User', on_delete=models.SET_NULL, null=True, blank=False, related_name='orders')
    discount = models.ForeignKey('products.Discount', on_delete=models.SET_NULL, null=True, blank=True)
    delivery = models.ForeignKey('delivery.Delivery', on_delete=models.SET_NULL, null=True, blank=False)
    status = models.CharField(max_length=64, choices=OrderStatus.choices, default=OrderStatus.PROCESS)
    created_at = models.DateTimeField(auto_now_add=True)  # CHECK IT
    updated_at = models.DateTimeField(auto_now=True)

    order_id = models.CharField(max_length=20, unique=True, editable=False)

    class Meta:
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        if not self.order_id:
            self.order_id = self.generate_order_id()
        return super().save(*args, **kwargs)

    async def asave(self, *args, **kwargs):
        if not self.order_id:
            self.order_id = self.generate_order_id()
        return await super().asave(*args, **kwargs)

    @staticmethod
    def generate_order_id():
        '''
            Generate humanized order id
        '''
        now = dt.datetime.now(dt.UTC)
        date_part = now.strftime("%y%j")
        get_random_part = lambda: random.choices(string.ascii_uppercase + string.digits, k=4)
        while True:
            # Compose new order id till it's not already exist in db
            random_part1 = ''.join(get_random_part())
            random_part2 = ''.join(get_random_part())
            order_number = f"{date_part}-{random_part1}-{random_part2}"

            if not Order.objects.filter(order_id=order_number).exists():
                return order_number


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey('products.Product', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=5)
    amount = models.IntegerField()
    discount = models.ForeignKey('products.Discount', on_delete=models.SET_NULL, null=True, blank=True)
