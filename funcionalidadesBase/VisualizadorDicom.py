import os
import tkinter as tk
from tkinter import filedialog
import pydicom as dicom
from PIL import Image, ImageTk

class VisualizadorDICOM:
    def __init__(self, root):
        self.root = root
        self.carpeta = None
        self.archivos_dicom = []
        self.indice_actual = 0

        self.boton_seleccionar = tk.Button(root, text="Seleccionar Carpeta", command=self.seleccionar_carpeta)
        self.boton_seleccionar.pack()

        self.boton_anterior = tk.Button(root, text="<< Anterior", command=self.mostrar_anterior, state=tk.DISABLED)
        self.boton_anterior.pack()

        self.boton_siguiente = tk.Button(root, text="Siguiente >>", command=self.mostrar_siguiente, state=tk.DISABLED)
        self.boton_siguiente.pack()

        self.etiqueta_imagen = tk.Label(root)
        self.etiqueta_imagen.pack()

    def seleccionar_carpeta(self):
        self.carpeta = filedialog.askdirectory()
        if self.carpeta:
            self.cargar_imagenes_dicom()

    def cargar_imagenes_dicom(self):
        self.archivos_dicom = [archivo for archivo in os.listdir(self.carpeta) if archivo.endswith('.dcm')]
        if self.archivos_dicom:
            self.mostrar_imagen()
            self.boton_anterior.config(state=tk.NORMAL)
            self.boton_siguiente.config(state=tk.NORMAL)

    def mostrar_imagen(self):
        if self.archivos_dicom:
            archivo = self.archivos_dicom[self.indice_actual]
            ds = dicom.dcmread(os.path.join(self.carpeta, archivo))
            imagen_pil = Image.fromarray(ds.pixel_array)
            imagen_redimensionada = imagen_pil.resize((800, 800))
            imagen_tk = ImageTk.PhotoImage(imagen_redimensionada)
            self.etiqueta_imagen.config(image=imagen_tk)
            self.etiqueta_imagen.image = imagen_tk

    def mostrar_anterior(self):
        if self.indice_actual > 0:
            self.indice_actual -= 1
            self.mostrar_imagen()

    def mostrar_siguiente(self):
        if self.indice_actual < len(self.archivos_dicom) - 1:
            self.indice_actual += 1
            self.mostrar_imagen()

# Crea la ventana principal de la aplicación
root = tk.Tk()
root.title("Visualizador de DICOM")

app = VisualizadorDICOM(root)

root.mainloop()
