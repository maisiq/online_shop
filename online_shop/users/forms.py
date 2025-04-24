from django.contrib.auth.forms import BaseUserCreationForm

from .models import User


class CreateUserForm(BaseUserCreationForm):

    class Meta:
        model = User
        fields = ['email']