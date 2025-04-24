from decimal import Decimal

import pytest
import pytest_asyncio
from django.conf import settings
from django.contrib.sessions.middleware import SessionMiddleware
from django.test import RequestFactory
from faker import Faker

from online_shop.cart.cart import Cart
from online_shop.products.models import Category, Product

CART_ID = settings.CART_ID

@pytest_asyncio.fixture
async def data():
    f = Faker('ru_RU')
    category = await Category.objects.acreate(name=f.word())
    return await Product.objects.acreate(
        category=category,
        name='Random product',
        price=Decimal('120.00'),
        currency='RUB',
        cover='asd',
        description='desc',
    )

@pytest.fixture
def request_with_session() -> Cart:
    factory = RequestFactory()
    request = factory.request()

    middleware = SessionMiddleware(lambda x: None)
    middleware.process_request(request)

    return request


@pytest.mark.django_db
def test_can_add_to_cart(data, request_with_session):
    
    cart = Cart(request_with_session.session)
    cart.add(str(data.id))

    expected_data = {
        'price': str(data.price),
        'amount': 1,
    }
    assert request_with_session.session[CART_ID][str(data.id)] == expected_data


@pytest.mark.django_db
def test_can_decrease(data, request_with_session):
    cart = Cart(request_with_session.session)
    cart.add(str(data.id), amount=5, overwrite=True)
    cart.decrease(str(data.id))
    cart.decrease(str(data.id))

    expected_data = {
        'price': str(data.price),
        'amount': 3,
    }

    assert request_with_session.session[CART_ID][str(data.id)] == expected_data

@pytest.mark.django_db
def test_delete_item_when_amount_zero(data, request_with_session):
    cart = Cart(request_with_session.session)
    cart.add(str(data.id))
    cart.decrease(str(data.id))

    assert request_with_session.session[CART_ID].get(str(data.id)) == None

@pytest.mark.django_db
def test_delete_item(data, request_with_session):
    cart = Cart(request_with_session.session)
    cart.add(str(data.id))
    cart.delete(str(data.id))

    assert request_with_session.session[CART_ID].get(str(data.id)) == None

@pytest.mark.django_db
def test_clear_cart(data, request_with_session):
    cart = Cart(request_with_session.session)
    cart.add(str(data.id))
    cart.clear()

    assert request_with_session.session[CART_ID] == {}


