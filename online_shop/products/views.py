from uuid import UUID

from django.conf import settings
from django.contrib import messages
from django.http import HttpRequest
from django.shortcuts import get_object_or_404, render

from online_shop.cart.cart import Cart
from online_shop.core.utils import redirect_back

from .forms import AddDiscountForm
from .models import Category, Discount, Product


def products(r: HttpRequest):
    products = Product.objects.all()

    context = {
        'products': products,
    }
    return render(r, 'index.html', context)


def product_detail(r: HttpRequest, product_id: UUID):
    product = get_object_or_404(Product, id=product_id)

    categories = Category.objects.all()
    context = {
        'product': product,
        'categories': categories,
    }

    return render(r, 'product.html', context)


def add_discount(r: HttpRequest):
    form = AddDiscountForm(r.POST)
    cart = Cart(r.session, settings.CURRENT_ORDER_KEY)
    if form.is_valid():
        discount = Discount.objects.filter(name=str.upper(form.cleaned_data['discount'])).first()
        cart.apply_discount(discount)
    else:
        messages.error(r, list(form.errors.values()))
    return redirect_back(r) 


def remove_discount(r: HttpRequest):
    cart = Cart(r.session, settings.CURRENT_ORDER_KEY)
    cart.remove_discount()
    return redirect_back(r)
