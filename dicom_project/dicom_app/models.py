from django.db import models

class DicomImage(models.Model):
    file = models.FileField(upload_to='dicom_files/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
