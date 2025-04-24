from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpRequest
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import FormView, View

from .forms import CreateUserForm


class CreateUserView(FormView):
    form_class = CreateUserForm
    success_url = reverse_lazy('products:list')
    template_name = 'signup.html'

    def post(self, r: HttpRequest, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            form.save()
            messages.info(r, 'Account succesfully created')
            return redirect(self.get_success_url())
        return self.render_to_response({'form': form})

    def get(self, r: HttpRequest, *args, **kwargs):
        form = self.get_form()
        return self.render_to_response({'form': form})
    

class AutheticationUserView(FormView):
    form_class = AuthenticationForm
    success_url = reverse_lazy('products:list')
    template_name = 'signin.html'

    def post(self, r: HttpRequest, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            login(r, form.get_user())
            messages.info(r, 'You are logged in')
            return redirect(self.get_success_url())
        return self.render_to_response({'form': form})

    def get(self, r: HttpRequest, *args, **kwargs):
        form = self.get_form()
        return self.render_to_response({'form': form})


class LogoutView(View):
    def post(self, r: HttpRequest, *args, **kwargs):
        if r.user.is_authenticated:
            messages.info(r, 'Logged out')
            logout(r)
        return redirect('products:list')