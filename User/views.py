from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.forms import AuthenticationForm
from django.urls import reverse_lazy


class UserLoginView(LoginView):
    template_name = 'user/login.html'
    form_class = AuthenticationForm


class UserLogOut(LogoutView):
    next = reverse_lazy('user:login')