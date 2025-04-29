from django.conf import settings
from django.http import HttpRequest
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView

from online_shop.core.utils import redirect_back

from .cart import Cart
from .forms import SelectItemsForm


class CartView(TemplateView):
    template_name = 'cart.html'

    def get(self, request, *args, **kwargs):
        cart = Cart(request.session)
        form = SelectItemsForm(items_id=cart.get_items_id())
        return self.render_to_response({'form': form})

    def post(self, request: HttpRequest, *args, **kwargs):
        cart = Cart(request.session)
        form = SelectItemsForm(items_id=cart.get_items_id(), data=request.POST)

        if form.is_valid():
            products = form.cleaned_data.get('items')
            for_order = Cart(request.session, settings.CURRENT_ORDER_KEY)
            for_order.clear()

            for product in products:
                product_id = str(product.id)
                for item in cart:
                    if item['product'] != product:
                        continue
                    for_order.add(product_id, amount=item['amount'], overwrite=True)

            return redirect('delivery:choose')
        return self.render_to_response({'form': form})


def cart(request: HttpRequest):
    cart = Cart(request.session)
    form = SelectItemsForm(items_id=cart.get_items_id())
    
    return render(request, 'cart.html', {'form': form})


@csrf_exempt
def add_to_cart(request: HttpRequest, product_id):
    cart = Cart(request.session)
    cart.add(str(product_id))

    return redirect_back(request)


@csrf_exempt
def decrease_amount(request: HttpRequest, product_id):
    cart = Cart(request.session)
    cart.decrease(str(product_id))

    return redirect_back(request)


@csrf_exempt
def delete_from_cart(request: HttpRequest, product_id):
    cart = Cart(request.session)
    cart.delete(str(product_id))

    return redirect_back(request)


@csrf_exempt
def clear_cart(request: HttpRequest):
    cart = Cart(request.session)
    cart.clear()

    return redirect_back(request)