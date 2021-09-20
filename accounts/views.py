from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.views.generic import CreateView

from accounts.forms import RegistrationForm


class LoginUser(LoginView):
    form_class = AuthenticationForm
    template_name = 'accounts/login.html'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('mycompany')


class RegisterUser(CreateView):
    form_class = RegistrationForm
    success_url = reverse_lazy('login')
    template_name = 'accounts/register.html'

