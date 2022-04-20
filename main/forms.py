from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django import forms
from django.forms import ModelForm, TextInput, Textarea
from .models import *


class RegisterUserForm(UserCreationForm):
    username = forms.CharField(label="Введите логин", widget=forms.TextInput()) # TODO: widgets
    password1 = forms.CharField(label="Введите пароль", widget=forms.PasswordInput())
    password2 = forms.CharField(label="Повторите пароль", widget=forms.PasswordInput())
    #email = forms.EmailField(label="Введите email", widget=forms.EmailInput())

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-input'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-input'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-input'}),
        }


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label="Имя пользователя", widget=forms.TextInput())
    password = forms.CharField(label="Пароль", widget=forms.PasswordInput())


class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content']
        widgets = {
            'title': TextInput(attrs={'class':'form-control', 'placeholder':'Название поста(необязательно)'}),
            'content': Textarea(attrs={'class': 'form-control', 'placeholder': 'Пишите пост...'})
        }


class RequestForm(forms.Form):
    user = forms.CharField(max_length=30)


