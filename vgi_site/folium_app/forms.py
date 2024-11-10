from django import forms
from .models import UploadedFile


class FileUpdateForm(forms.ModelForm):
    class Meta:
        model = UploadedFile
        fields = ('file',)

class FileUploadForm(forms.ModelForm):
    class Meta:
        model = UploadedFile
        fields = ['file']  # Ensure this matches your model field
