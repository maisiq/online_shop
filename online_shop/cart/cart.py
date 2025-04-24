import copy
import uuid
from collections.abc import Iterator
from dataclasses import dataclass
from decimal import Decimal

from django.conf import settings
from django.contrib.sessions.backends.base import SessionBase

from online_shop.products.models import Product


@dataclass
class ProductDTO:
    product: Product
    price: Decimal
    amount: int


class Cart:
    def __init__(self, session: SessionBase, session_key: str = settings.CART_ID):
        self.__session = session
        self.__session_key = session_key
        cart = self.__session.get(self.__session_key)

        if cart is None:
            self.__cart = self.__session[self.__session_key] = {}
        else:
            self.__cart = cart

    def add(self, product_id: str, amount: int = 1, overwrite: bool = False):
        try:
            product_uuid = uuid.UUID(product_id)
        except ValueError:
            return

        product = Product.objects.filter(id=product_uuid).first()
        if not product:
            return
        if product_id in self.__cart and not overwrite:
            self.__cart[product_id]['amount'] += 1
        else:
            self.__cart[product_id] = {'price': str(product.price), 'amount': amount}
        self._save()

    def decrease(self, product_id: str):
        if product_id in self.__cart:
            amount = self.__cart[product_id]['amount']
            if amount <= 1:
                self.delete(product_id)
            else:
                self.__cart[product_id]['amount'] -= 1
            self._save()

    def delete(self, product_id: str) -> None:
        if product_id in self.__cart:
            del self.__cart[product_id]
            self._save()
    
    def clear(self):
        self.__cart = self.__session[self.__session_key] = {}
        self._save()

    def total(self):
        full_price = 0
        for item in self.__cart.values():
            full_price += item['amount'] * Decimal(item['price'])
        return full_price

    def get_items_id(self):
        return self.__cart.keys()

    def _save(self):
        self.__session.modified = True

    def __iter__(self) -> Iterator[ProductDTO]:

        products = Product.objects.in_bulk(self.__cart.keys())
        cart = copy.deepcopy(self.__cart)

        def fn(k, v):
            # add `Product` object for fast access to it in templates e.g.
            cart[str(k)]['product'] = v
            return cart[str(k)]

        return (fn(k, v) for k, v in products.items())

    def __contains__(self, value):
        return value in self.__cart
    
    def __len__(self):
        return len(self.__cart)

    
