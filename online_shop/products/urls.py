from django.urls import path

from .views import product_detail, products

app_name = 'products'

urlpatterns = [
    path('', products, name='list'),
    path('<uuid:product_id>/', product_detail, name='detail'),
]