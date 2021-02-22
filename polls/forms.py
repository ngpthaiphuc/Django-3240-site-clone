from django import forms

from .models import Thought

class InputForm(forms.ModelForm):
    class Meta:
        model = Thought
        fields = ["title_field", "description_field",]
        labels = {"title_field": "Thought Title", "description_field": "Description",}