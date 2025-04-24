from urllib.parse import urlencode

from django.conf import settings
from django.http import HttpRequest, JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.generic import ListView, View

from online_shop.cart.cart import Cart
from online_shop.delivery.forms import OptDeliveryForm

from .models import Order, OrderItem


class OrderListView(ListView):
    model = Order
    template_name = 'order_list.html'
    context_object_name = 'orders'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)

        cart = Cart(self.request.session)
        ctx['cart'] = cart
        return ctx

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(customer=self.request.user).prefetch_related('items').all()


class CreateOrderView(View):
    def post(self, request: HttpRequest, *args, **kwargs):
        form = OptDeliveryForm(user=request.user, data=request.POST)

        if form.is_valid():
            cart = Cart(request.session, settings.CURRENT_ORDER_KEY)
            order = Order.objects.create(
                customer=request.user,
                delivery=form.cleaned_data['delivery'],
            )
            for item in cart:
                order_item = OrderItem.objects.create(
                    order=order,
                    product=item['product'],
                    price=item['price'], # fix?
                    currency=item['product'].currency,  # fix
                    amount=item['amount'],
                    # discount=...
                )
            base_redirect_url = reverse('payment:stripe_session')
            query_string = urlencode({'order_id': order.order_id})
            return redirect(f'{base_redirect_url}?{query_string}')
        return JsonResponse({'detail': 'Validation error'})
