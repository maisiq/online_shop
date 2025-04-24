import datetime as dt

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models.manager import BaseManager
from mptt.models import MPTTModel, TreeForeignKey
from slugify import slugify
from uuid_extensions import uuid7


class Category(MPTTModel):
    name = models.CharField(max_length=128)
    slug = models.SlugField(primary_key=True, blank=True)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, related_name='subcategory', null=True, blank=True)

    class MPTTMeta:
        order_insertion_by = ['name']

    class Meta:
        verbose_name_plural = 'categories'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)
    
    # async def asave(self, force_insert = ..., force_update = ..., using = ..., update_fields = ...):
    #     if not self.slug:
    #         self.slug = slugify(self.name)
    #     return await super().asave(force_insert=force_insert, force_update=force_update, using=using, update_fields=update_fields)

    def __str__(self):
        return self.name


def product_image_path(instance, filename):
    return f'data/products/{instance.category.slug}/{filename}'


class Product(models.Model):
    id = models.UUIDField(default=uuid7, primary_key=True, editable=False) # change to uuidv7
    name = models.CharField(
        verbose_name='product name', 
        max_length=256, blank=False, 
        null=False,
    )
    price = models.DecimalField(
        validators=[MinValueValidator(0)],
        max_digits=10,
        decimal_places=2,
    )
    currency = models.CharField(max_length=5)
    cover = models.ImageField(upload_to=product_image_path)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=False)
    discount = models.ForeignKey('products.Discount', on_delete=models.SET_NULL, null=True, blank=True)


class Discount(models.Model):
    class DiscountType(models.TextChoices):
        PRODUCT_WIDE = 'product'
        ORDER_WIDE = 'order'
        PERSONAL = 'personal'

    type = models.CharField(max_length=64, choices=DiscountType.choices)
    name = models.CharField(max_length=128)
    value = models.IntegerField(
        validators=[
            MinValueValidator(1, 'Value should be 1 atleast'),
            MaxValueValidator(100, 'Discount value cant be more than 100')
        ],
    )
    start_at = models.DateTimeField()
    expired_at = models.DateTimeField()

    @property
    def is_active(self) -> bool:
        now = dt.datetime.now(dt.UTC)
        if now > self.start_at and now < self.expired_at:
            return True
        return False

    # check DateTime format in save method
