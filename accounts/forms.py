from django import forms
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User


class RegistrationForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'password')

    def clean_password(self):
        password = self.cleaned_data['password']
        return make_password(password)
