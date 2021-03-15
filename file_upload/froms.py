from django import forms
from .models import Image,Document



class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ('title','description','version', 'document')
