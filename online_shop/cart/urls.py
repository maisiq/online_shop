from django.urls import path

from .views import CartView, add_to_cart, clear_cart, decrease_amount, delete_from_cart

app_name = 'cart'

urlpatterns = [
    path('', CartView.as_view(), name='cart'),
    path('add/<uuid:product_id>/', add_to_cart, name='add'),
    path('decrease/<uuid:product_id>/', decrease_amount, name='decrease'),
    path('delete/<uuid:product_id>/', delete_from_cart, name='delete'),
    path('clear/', clear_cart, name='clear'),
]
