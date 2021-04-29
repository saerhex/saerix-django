from django import forms
from . import models


class AddArticleForm(forms.ModelForm):
    class Meta:
        model = models.Article
        fields = ('user',
                  'title',
                  'text')


class UpdateArticleForm(forms.ModelForm):
    class Meta:
        model = models.Article
        fields = ('title',
                  'text')
