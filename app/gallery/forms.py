from django import forms
from . import models


class CreateCommentary(forms.ModelForm):
    class Meta:
        model = models.Commentary
        fields = ('text', )
