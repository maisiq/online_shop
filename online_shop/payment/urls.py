from django.urls import path

from .views.stripe import create_checkout_session, success, webhook

app_name = 'payment'

urlpatterns = [
    path('create-checkout-session/', create_checkout_session, name='stripe_session'),
    path('stripe/success/', success, name='stripe_success'),
    path('stripe/webhook/', webhook, name='stripe_webhook'),
]
