import logging

import requests
from django.conf import settings
from django.http import HttpRequest
from django.http.response import JsonResponse
from django.urls import reverse_lazy
from django.views.generic import FormView

from online_shop.cart.cart import Cart
from online_shop.products.forms import AddDiscountForm

from .config import cdek_settings
from .forms import CreateDeliveryForm, OptDeliveryForm
from .models import Delivery
from .utils import get_cdek_token


def cdek_deliverypoints(request: HttpRequest):
    '''
    Returns list of delivery points from CDEK API.
    Points can be used for interative map in frontend

    Response from cdek_settings.SUGGEST_CITIES_URL returns list of dicts with format:
        {'code': int, 'city_uuid': str, 'full_name': str}
    '''

    city = request.GET.get('city')
    city_code = 44  # Moscow by default

    access_token = get_cdek_token()

    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }
    if city:
        options = requests.get(cdek_settings.SUGGEST_CITIES_URL.format(city), headers=headers)
        match options.status_code:
            case 401:
                logging.error({'error': 'Unauthorized', 'detail': 'Invalid token for CDEK API'})
            case 200:
                city_code = options.json()[0].get('code') or city_code
            case _:
                logging.error({
                    'error': 'Unexpected response from CDEK API', 
                    'status_code': options.status_code,
                    'detail': options.text,
                })

    response = requests.get(cdek_settings.API_URL + f'&city_code={city_code}', headers=headers)

    if response.status_code == 200:
        return JsonResponse(response.json(), safe=False)
    logging.error({'error': 'Ошибка запроса к CDEK API', 'detail': response.json()})
    return JsonResponse({"error": "Ошибка запроса к CDEK"}, status=response.status_code)


class OptDeliveryView(FormView):
    template_name = 'opt_delivery.html'
    form_class = OptDeliveryForm
    success_url = reverse_lazy('orders:create')
    
    def get(self, request: HttpRequest, *args, **kwargs):
        form: OptDeliveryForm = self.get_form()
        add_delivery_form = AddDiscountForm()
        items = Cart(request.session, settings.CURRENT_ORDER_KEY)
        return self.render_to_response({'form': form, 'order_items': items, 'add_delivery_form': add_delivery_form})

    def get_form_kwargs(self) -> dict:
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user  # pass User instance to form initialization
        return kwargs


class AddDeliveryView(FormView):
    model = Delivery
    form_class = CreateDeliveryForm
    template_name = 'create_delivery.html'
    success_url = reverse_lazy('delivery:choose')

    def get(self, request: HttpRequest, *args, **kwargs):
        return self.render_to_response({'form': self.get_form()})

    def form_valid(self, form: CreateDeliveryForm):
        form.instance.customer = self.request.user
        form.save()
        return super().form_valid(form)

    def get_success_url(self):
        return super().get_success_url()