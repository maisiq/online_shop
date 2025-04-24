from django.urls import path

from .views import AutheticationUserView, CreateUserView, LogoutView

app_name = 'users'

urlpatterns = [
    path('signup/', CreateUserView.as_view(), name='signup'),
    path('signin/', AutheticationUserView.as_view(), name='signin'),
    path('logout/', LogoutView.as_view(), name='logout'),
]
