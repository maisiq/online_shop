from django.http import HttpRequest
from django.shortcuts import redirect


def redirect_back(r: HttpRequest):
    redirect_to = r.META.get('HTTP_REFERER', '/')
    return redirect(redirect_to)