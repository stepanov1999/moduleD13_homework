import uuid
from datetime import timedelta

from django.contrib.auth.forms import (
    AuthenticationForm,
    UserCreationForm,
    UserChangeForm,
)
from .models import User, EmailVerification, Comment
from django import forms
from django.utils.timezone import now


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control py-4",
                "placeholder": "Введите имя пользователя",
            }
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"class": "form-control py-4", "placeholder": "Введите пароль"}
        )
    )

    class Meta:
        model = User
        fields = ("username", "password")


class UserRegisterForm(UserCreationForm):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control py-4",
                "placeholder": "Введите имя пользователя",
            }
        )
    )
    email = forms.CharField(
        widget=forms.EmailInput(
            attrs={
                "class": "form-control py-4",
                "placeholder": "Введите адрес эл. почты",
            }
        )
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"class": "form-control py-4", "placeholder": "Введите пароль"}
        )
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"class": "form-control py-4", "placeholder": "Подтвердите пароль"}
        )
    )

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super().save(commit)
        expiration = now() + timedelta(hours=48)
        record = EmailVerification.objects.create(
            code=uuid.uuid4(), user=user, expiration=expiration
        )
        record.send_verefication_email()
        return user


class UserProfileForm(UserChangeForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control py-4"})
    )
    email = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control py-4", "readonly": True})
    )
    image = forms.ImageField(
        widget=forms.FileInput(attrs={"class": "custom-file-label"}), required=False
    )

    class Meta:
        model = User
        fields = ("username", "email", "image")


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ("text",)
