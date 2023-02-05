from django import forms
from django.core import validators


class SignUp(forms.Form):
    first_name = forms.CharField(initial = 'First Name', required=True)
    email = forms.EmailField(initial = 'Enter your email', required=True, validators=[validators.EmailValidator(message="Invalid Email")])
