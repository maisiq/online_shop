from urllib.parse import urlencode

from django.conf import settings
from django.http import HttpRequest, JsonResponse
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import ListView, View

from online_shop.cart.cart import Cart
from online_shop.delivery.forms import OptDeliveryForm

from .models import Order, OrderItem


class OrderListView(ListView):
    model = Order
    template_name = 'order_list.html'
    context_object_name = 'orders'

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
                discount=cart.get_discount()
            )
            for item in cart:
                OrderItem.objects.create(
                    order=order,
                    product=item['product'],
                    price=item['price'],
                    currency=item['product'].currency,
                    amount=item['amount'],
                )
            cart.clear()
            base_redirect_url = reverse('payment:stripe_session')
            query_string = urlencode({'order_id': order.order_id})
            return redirect(f'{base_redirect_url}?{query_string}')
        return JsonResponse({'detail': 'Validation error'})
