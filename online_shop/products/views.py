from uuid import UUID

from django.http import HttpRequest
from django.shortcuts import get_object_or_404, render

from online_shop.cart.cart import Cart
from online_shop.products.models import Category, Product


def products(r: HttpRequest):
    cart = Cart(r.session)
    products = Product.objects.all()

    context = {
        'cart': cart,
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
