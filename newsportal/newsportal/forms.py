from django import forms
from django.core.exceptions import ValidationError

from .models import Post


class PostForm(forms.ModelForm):
    # description = forms.CharField(min_length=20)

    class Meta:
        model = Post
        fields = [
            'title',
            'content',
            'author',
        ]

    # def clean(self):
    #     cleaned_data = super().clean()
    #     description = cleaned_data.get("description")
    #     name = cleaned_data.get("name")
    #
    #     if name == description:
    #         raise ValidationError(
    #             "Описание не должно быть идентичным названию."
    #         )
    #
    #     return cleaned_data
    #
    # def clean_name(self):
    #     name = self.cleaned_data["name"]
    #     if name[0].islower():
    #         raise ValidationError(
    #             "Название должно начинаться с заглавной буквы."
    #         )
    #     return name
