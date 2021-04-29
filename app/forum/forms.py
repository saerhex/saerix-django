from django import forms
from . import models


class CreateInDiscussion(forms.ModelForm):
    class Meta:
        model = models.Discussion
        fields = ('user',
                  'title',
                  'description')
