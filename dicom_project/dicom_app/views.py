from django.shortcuts import render
import pydicom
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import DicomImage

@csrf_exempt
def upload_dicom(request):
    if request.method == 'POST' and 'file' in request.FILES:
        dicom_file = request.FILES['file']
        dicom_image = DicomImage.objects.create(file=dicom_file)
        
        # Procesar el archivo DICOM
        dicom_data = pydicom.dcmread(dicom_image.file.path)
        metadata = {key: str(dicom_data.data_element(key)) for key in dicom_data.dir()}
        
        return JsonResponse({'metadata': metadata})
    return JsonResponse({'error': 'Invalid request'}, status=400)
