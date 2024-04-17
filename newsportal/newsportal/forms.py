from allauth.account.forms import SignupForm
from django import forms
from django.contrib.auth.models import Group, User

from .models import Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = [
            'title',
            'content',
            'author',
            'categories',
        ]
