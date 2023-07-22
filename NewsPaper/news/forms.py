from django import forms
from .models import Post, Author
from django.core.exceptions import ValidationError


class PostForm(forms.ModelForm):
    title = forms.CharField(min_length=20)  # В самом поле поставили ограничение на минимальную длину

    class Meta:
        model = Post
        fields = [
            'author',
            'text',
            'title',
            'choice',
            #'posting_time',
            'category',
            'post_rating',
        ]  # можно прописать __all__

        def clean(self):  # Мы переопределили метод clean и реализовали в нём проверку.
            cleaned_data = super().clean()
            text = cleaned_data.get("text")
            title = cleaned_data.get("title")

            if text == title:
                raise ValidationError(
                    "Текст не должен быть идентичен названию."
                )
            return cleaned_data
