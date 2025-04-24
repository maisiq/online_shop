from django.urls import path

from .views import CreateOrderView, OrderListView

app_name = 'orders'

urlpatterns = [
    path('create/', CreateOrderView.as_view(), name='create'),
    path('', OrderListView.as_view(), name='list'),
]
