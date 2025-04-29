from django.urls import path

from .views import add_discount, product_detail, products, remove_discount

app_name = 'products'

urlpatterns = [
    path('', products, name='list'),
    path('<uuid:product_id>/', product_detail, name='detail'),
    path('discount/', add_discount, name='discount'),
    path('discount-remove/', remove_discount, name='discount_remove'),
]