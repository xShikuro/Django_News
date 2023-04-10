from django import forms

from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from .models import Article, Comment


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["content"]
        widgets = {
            "content": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 5
            })
        }


class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ["title", "description", "image", "category"]
        widgets = {
            "title": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Напишите название статьи"
            }),
            "description": forms.Textarea(attrs={
                "class": "form-control",
                "placeholder": "Напишите описание статьи"
            }),
            "image": forms.FileInput(attrs={
                "class": "form-control"
            }),
            "category": forms.Select(attrs={
                "class": "form-select"
            })
        }



class LoginForm(AuthenticationForm):
    username = forms.CharField(label="Имя пользователя",
                               widget=forms.TextInput(attrs={
                                   "class": "form-control"
                               }))
    password = forms.CharField(label="Пароль", widget=forms.PasswordInput(attrs={
        "class": "form-control"
    }))

    class Meta:
        model = User


class RegistrationForm(UserCreationForm):
    username = forms.CharField(label="Имя пользователя",
                               help_text=None,
                               widget=forms.TextInput(attrs={
                                   "class": "form-control"
                               }))
    password1 = forms.CharField(label="Пароль", widget=forms.PasswordInput(attrs={
        "class": "form-control"
    }))
    password2 = forms.CharField(label="Подтвердите Пароль", widget=forms.PasswordInput(attrs={
        "class": "form-control"
    }))

    class Meta:
        model = User
        fields = ["username", "email"]
        widgets = {
            "email": forms.EmailInput(attrs={
                "class": "form-control"
            })
        }