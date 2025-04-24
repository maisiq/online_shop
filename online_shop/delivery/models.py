from django.db import models
from uuid_extensions import uuid7


class Delivery(models.Model):
    class DeliveryTypes(models.TextChoices):
        CDEK = 'cdek'
        RussianPost = 'russian_mail'

    id = models.CharField(primary_key=True, default=uuid7, max_length=128)
    type = models.CharField(max_length=128, choices=DeliveryTypes.choices)
    address = models.TextField()
    receiver = models.TextField()
    receiver_phone = models.CharField(max_length=64)
    customer = models.ForeignKey('users.User', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.type} {self.receiver} {self.address} {self.receiver_phone}'