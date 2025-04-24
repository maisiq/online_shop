from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('cart/', include('online_shop.cart.urls')),
    path('', include('online_shop.products.urls')),
    path('order/', include('online_shop.orders.urls')),
    path('delivery/', include('online_shop.delivery.urls')),
    path('payment/', include('online_shop.payment.urls')),
    path('users/', include('online_shop.users.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
