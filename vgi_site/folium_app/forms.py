from django import forms
from .models import UploadedFile

class FileUploadForm(forms.ModelForm):
    class Meta:
        model = UploadedFile
        fields = ['file']  # Ensure this matches your model field

    file = forms.FileField(
        widget=forms.ClearableFileInput(attrs={"accept": ".xml"})
    )

