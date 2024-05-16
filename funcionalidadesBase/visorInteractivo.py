import os
import pydicom as dicom
import matplotlib.pyplot as plt

def visualizar_imagenes_dicom(carpeta):
    # Lista todos los archivos en la carpeta
    archivos = os.listdir(carpeta)
    
    # Filtra solo los archivos DICOM
    archivos_dicom = [archivo for archivo in archivos if archivo.endswith('.dcm')]
    
    # Itera sobre cada archivo DICOM
    for archivo in archivos_dicom:
        # Lee el archivo DICOM
        ds = dicom.dcmread(os.path.join(carpeta, archivo))
        
        # Visualiza la imagen
        plt.imshow(ds.pixel_array, cmap=plt.cm.bone)
        plt.title(f"{archivo} - {ds.PatientName}")
        plt.show()

# Especifica la ruta de la carpeta donde están los archivos DICOM
carpeta_dicom = 'funcionalidadesbase\imagenes'

# Llama a la función para visualizar las imágenes
visualizar_imagenes_dicom(carpeta_dicom)
