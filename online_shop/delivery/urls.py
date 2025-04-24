from django.urls import path

from .views import AddDeliveryView, OptDeliveryView, cdek_deliverypoints

app_name = 'delivery'

urlpatterns = [
    path('choose/', OptDeliveryView.as_view(), name='choose'),
    path('create/', AddDeliveryView.as_view(), name='create'),
    path('api/cdek/', cdek_deliverypoints, name='cdek_deliverypoints'),
]
