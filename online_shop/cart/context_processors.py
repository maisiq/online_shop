from django.http import HttpRequest

from .cart import Cart


def cart(r: HttpRequest):
    return {
        'cart': Cart(r.session)
    }