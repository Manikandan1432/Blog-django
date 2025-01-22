from django import forms
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.shortcuts import redirect
class ContactForm(forms.Form):
    name = forms.CharField(label='name', max_length=200)
    email = forms.EmailField(label='email', max_length=100)
    message = forms.CharField(label='message')


class RegisterForm(forms.ModelForm):
    username = forms.CharField(label='username', max_length=100, required=True)
    email = forms.EmailField(label='email', required=True)
    password = forms.CharField(label='password', max_length=100, required=True)
    password_confirm = forms.CharField(label='confirm_password', max_length=100, required=True)

    class Meta:
        model = User
        fields = [
            'username', 'email', 'password'
        ]

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')

        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError('Password does not match')

class LoginForm(forms.Form):
    username = forms.CharField(max_length=200)
    password = forms.CharField(max_length=200)

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')

        if username and password:
            user = authenticate(username=username, password=password)
            if user is None:
                raise forms.ValidationError('Invalid Username or Password')