from django.db import models

def validate_file_extension(value):
    if not value.name.endswith('.xml'):
        raise TypeError('file is not an xml')


class UploadedFile(models.Model):
    file = models.FileField(upload_to='uploads/')  # Save files in the 'uploads/' directory
    uploaded_at = models.DateTimeField(auto_now_add=True, validators=[validate_file_extension])


