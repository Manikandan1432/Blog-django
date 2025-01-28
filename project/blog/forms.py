from django import forms
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.shortcuts import redirect
from .models import *
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

class ForgotPasswordForm(forms.Form):
    email = forms.EmailField(max_length=200, required=True)

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        if not User.objects.filter(email=email).exists():
            raise forms.ValidationError('Email does not register')

class ResetPasswordForm(forms.Form):
    new_password = forms.CharField(label='new_password', max_length=200, required=True)
    confirm_password = forms.CharField(label='confirm_password', max_length=200, required=True)

    def clean(self):
        cleaned_data = super().clean()
        new_password = cleaned_data.get('new_password')
        confirm_password = cleaned_data.get('confirm_password')

        if new_password and confirm_password and new_password != confirm_password:
            raise forms.ValidationError('password does not match')

class NewPost(forms.ModelForm):
    title = forms.CharField(label='title', max_length=200, required=True)
    content = forms.CharField(label='content', required=True)
    category = forms.ModelChoiceField(required=True, queryset=Category.objects.all())
    img_url = forms.ImageField(label='Image', required=False)
    class Meta:
        model = Datas
        fields = [
            'title',
            'content',
            'category',
            'img_url'
        ]

    def clean(self):
        cleaned_data = super().clean()
        title = cleaned_data.get('title')
        content = cleaned_data.get('content')

        if title and len(title) < 5:
            raise forms.ValidationError('title must be minimum 5 characters')

        if content and len(content) < 10:
            raise forms.ValidationError('content must be minimum 10 characters')

    def save(self, commit=...):
        post = super().save(commit)
        cleaned_data = super().clean()
        if cleaned_data.get('img_url'):
            post.img_url = cleaned_data.get('img_url')
        else:
            img_url = 'https://www.freeiconspng.com/uploads/no-image-icon-21.png'
            post.img_url = img_url
        if commit:
            post.save()
        return post
