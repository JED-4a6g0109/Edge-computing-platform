from django import forms
from .models import Image,Document

# class ImageForm(forms.ModelForm):
#     """Form for the image model"""
#     class Meta:
#         model = Image
#         fields = ('title', 'image')





class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ('title','description','version', 'document')
