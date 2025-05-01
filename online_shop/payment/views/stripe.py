import json
import logging
from decimal import ROUND_HALF_UP, Decimal

import stripe
from django.http import Http404, HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import redirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from online_shop.orders.models import Order
from online_shop.payment.config import stripe_config

stripe.api_key = stripe_config.API_KEY


# @require_POST
def create_checkout_session(r: HttpRequest):
    if not (order_id := r.GET.get('order_id')):
        raise Http404('Order id не передан')
    try:
        order = Order.objects.prefetch_related('items__product').get(order_id=order_id)
        line_items = []
        coupon = None

        for item in order.items.all():
            data = {
                'price_data': {
                    'currency': item.currency,
                    'product_data': {'name': item.product.name},
                    'unit_amount': int((item.price * 100).quantize(Decimal('1'), rounding=ROUND_HALF_UP)),
                },
                'quantity': item.amount
            }
            line_items.append(data)

        if order.discount:
            coupon = stripe.Coupon.create(
                percent_off=order.discount.value,
                duration='once'
            )

        checkout_session = stripe.checkout.Session.create(
            line_items=line_items,
            mode='payment',
            success_url=r.build_absolute_uri(reverse('payment:stripe_success')),
            cancel_url=r.build_absolute_uri('/cancel.html'),
            metadata={
                'order_id': order_id
            },
            discounts=[{
                'coupon': coupon and coupon.id,
            }],
            # currency='rub',
        )
    except Exception as e:
        logging.error(e)
        return redirect('/')

    return redirect(checkout_session.url, code=303)


def success(r: HttpRequest):
    return JsonResponse({'success': True})

@require_POST
@csrf_exempt
def webhook(r: HttpRequest):
    '''
    More about Stripe's event types: https://docs.stripe.com/api/events/types
    '''
    payload = r.body
    event = None

    sig_header = r.headers.get('Stripe-Signature')

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, stripe_config.WEBHOOK_SECRET
        )
    except stripe.SignatureVerificationError:
        return HttpResponse(status=400)

    # Handle the event
    match event.type:
        case 'checkout.session.completed':
            checkout_session_completed: stripe.PaymentIntent = event.data.object 
            if order_id := checkout_session_completed.metadata.get('order_id'):
                order = Order.objects.get(order_id=order_id)
                order.paid = True
                order.save()
                logging.info({'event': 'stripe_payment_completed', 'order': str(order.id)})
        case _:
            logging.info({'event': event.type, 'detail': event.data})
    return HttpResponse(status=200)
