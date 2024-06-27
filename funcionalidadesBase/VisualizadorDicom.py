import PySimpleGUI as sg
import pydicom
import cv2
import numpy as np
import os
from pydicom.uid import UID

# Función para leer un archivo DICOM y obtener la imagen y la información DICOM
def leer_dicom(ruta_dicom):
    try:
        # Leer el archivo DICOM
        ds = pydicom.dcmread(ruta_dicom)
        # Obtener la imagen DICOM como una matriz de píxeles
        img_data = ds.pixel_array
        # Normalizar la imagen para asegurar valores en el rango 0-255
        img_data = cv2.normalize(img_data, None, 0, 255, cv2.NORM_MINMAX)
        # Convertir a 8 bits
        img_data = np.uint8(img_data)
        return img_data, str(ds), ds
    except Exception as e:
        sg.popup_error(f"Error al abrir el archivo DICOM: {e}")
        return None, None

# Función para obtener la lista de archivos DICOM en una carpeta y su índice
def obtener_archivos_dicom_en_carpeta(ruta_carpeta):
    archivos_dicom = [archivo for archivo in os.listdir(ruta_carpeta) if archivo.lower().endswith('.dcm')]
    return archivos_dicom

# Función para redimensionar la imagen al tamaño deseado
def redimensionar_imagen(img_data, nuevo_ancho, nuevo_alto):
    img_resized = cv2.resize(img_data, (nuevo_ancho, nuevo_alto), interpolation=cv2.INTER_AREA)
    _, img_png = cv2.imencode('.png', img_resized)
    return img_png.tobytes()

# Función para aplicar filtros a los datos DICOM
def filtrar_datos_dicom(ds, filtro, valor):
    resultados = []
    for elem in ds:
        if filtro == "Nombre Dato" and elem.name.replace("'","").lower().find(valor.replace("'","").lower()) != -1:
            if elem.VR == "SQ":
                resultados.append("------------------")
                for e in elem:
                    resultados.append(f"    {e}")
                resultados.append("------------------")
            else:
                resultados.append(elem)
        elif filtro == "Grupo DICOM" and valor in f"{elem.tag.group:04x}":
            if elem.VR == "SQ":
                resultados.append("------------------")
                for e in elem:
                    resultados.append(f"    {e}")
                resultados.append("------------------")
            else:
                resultados.append(elem)
        elif filtro == "Número de elemento" and valor in f"{elem.tag.element:04x}":
            if elem.VR == "SQ":
                resultados.append("------------------")
                for e in elem:
                    resultados.append(f"    {e}")
                resultados.append("------------------")
            else:
                resultados.append(elem)
        elif filtro == "Tipo de valor" and elem.VR == valor.upper():
            if elem.VR == "SQ":
                resultados.append("------------------")
                for e in elem:
                    resultados.append(f"    {e}")
                resultados.append("------------------")
            else:
                resultados.append(elem)
    return resultados

# Define el diseño de la ventana principal
layout = [
    [sg.Text("Seleccione la carpeta de trabajo")],
    [sg.InputText(key="-FOLDER-"), sg.FolderBrowse("Seleccionar carpeta")],
    [sg.Button("Cargar carpeta")]
]

# Crea la ventana principal
window = sg.Window("Selección de archivos", layout)
filtros_disponibles = ["Nombre Dato", "Grupo DICOM", "Número de elemento", "Tipo de valor"]


# Bucle principal para interactuar con la ventana principal
while True:
    event, values = window.read()
    if event == sg.WINDOW_CLOSED:
        break # Detiene el bucle principal
    elif event == "Cargar carpeta":
        # Obtiene la ruta de la carpeta seleccionada
        carpeta_seleccionada = values["-FOLDER-"]
        # Verifica si se seleccionó una carpeta
        if carpeta_seleccionada:
            # Cierra la ventana de selección de carpeta
            window.close()
            # Obtiene la lista de archivos DICOM en la carpeta seleccionada
            archivos_dicom = obtener_archivos_dicom_en_carpeta(carpeta_seleccionada)
            if archivos_dicom:
                # Si hay archivos DICOM en la carpeta, preguntamos al usuario cuál desea abrir
                if len(archivos_dicom) == 1:
                    indice_imagen_seleccionada = 0  # Si hay solo una imagen, la seleccionamos automáticamente
                else:
                    layout_seleccion_imagen = [
                        [sg.Text("Seleccione la imagen a inicializar:")],
                        [sg.Listbox(values=archivos_dicom, size=(50, len(archivos_dicom)), key="-IMAGE_LIST-")],
                        [sg.Button("Abrir Imagen")]
                    ]
                    ventana_seleccion_imagen = sg.Window("Seleccionar Imagen", layout_seleccion_imagen)
                    event, values = ventana_seleccion_imagen.read()
                    if event == "Abrir Imagen" and values["-IMAGE_LIST-"]:
                        indice_imagen_seleccionada = archivos_dicom.index(values["-IMAGE_LIST-"][0])
                    else:
                        ventana_seleccion_imagen.close()
                        continue
                    ventana_seleccion_imagen.close()
                # Lee el archivo DICOM seleccionado
                img_data, info_dicom, ds = leer_dicom(os.path.join(carpeta_seleccionada, archivos_dicom[indice_imagen_seleccionada]))
            
                if img_data is not None and info_dicom is not None:
                    # Define el diseño de la ventana de visualización de la imagen DICOM

                    layout_imagen_dicom = [
                        [sg.Text(archivos_dicom[indice_imagen_seleccionada], key="-FILENAME-", size=(80, 1), justification='center', expand_x=True),
                         sg.Text("Buscar: "), sg.InputText(key="-SEARCH-", size=(20, 1), justification='right'), 
                         sg.Combo(filtros_disponibles, default_value=filtros_disponibles[0], key="-FILTER-", enable_events=True, readonly=True),
                         sg.Button("Buscar", key="-BUTTON-", size=(10, 1))],
                        [sg.Image(key="-IMAGE-", background_color="black", expand_x=True, expand_y=True),
                         sg.Multiline(key="-INFO-", size=(50, 20), expand_x=True, expand_y=True, disabled=True)],
                        [sg.Button("🡸", key="-PREV-", size=(15, 1)), sg.Button("🡺", key="-NEXT-", size=(15, 1))]
                    ]

                    # Crea la ventana de visualización de la imagen DICOM
                    window_imagen_dicom = sg.Window(
                        "Imagen DICOM", 
                        layout_imagen_dicom, 
                        finalize=True, 
                        resizable=True, 
                        size=(1850, 925)  # Tamaño inicial de la ventana
                    )

                    # Establece el índice de la imagen actual
                    indice_actual = indice_imagen_seleccionada
                    while True:
                        # Lee el archivo DICOM seleccionado
                        img_data, info_dicom, ds = leer_dicom(os.path.join(carpeta_seleccionada, archivos_dicom[indice_actual]))
                        if img_data is not None and info_dicom is not None:
                            # Redimensiona la imagen al tamaño inicial deseado (por ejemplo, 1000x800)
                            img_resized = redimensionar_imagen(img_data, 800, 800)
                            # Muestra la imagen y la información DICOM actual
                            window_imagen_dicom["-IMAGE-"].update(data=img_resized)
                            window_imagen_dicom["-INFO-"].update(value=info_dicom)
                            window_imagen_dicom["-FILENAME-"].update(value=archivos_dicom[indice_actual])
                        # Espera eventos de la ventana de imagen DICOM
                        event_imagen, values_imagen = window_imagen_dicom.read()
                        if event_imagen == sg.WINDOW_CLOSED:
                            break
                        elif event_imagen in ("-PREV-", "-NEXT-"):
                            # Cambia a la imagen DICOM anterior o siguiente
                            if event_imagen == "-PREV-":
                                indice_actual -= 1
                                if indice_actual < 0:
                                    indice_actual = len(archivos_dicom) - 1
                            elif event_imagen == "-NEXT-":
                                indice_actual += 1
                                if indice_actual >= len(archivos_dicom):
                                    indice_actual = 0
                            
                            # Lee el archivo DICOM seleccionado
                            img_data, info_dicom, ds = leer_dicom(os.path.join(carpeta_seleccionada, archivos_dicom[indice_actual]))
                            if img_data is not None and info_dicom is not None:
                                # Redimensiona la imagen al tamaño inicial deseado (por ejemplo, 1000x800)
                                img_resized = redimensionar_imagen(img_data, 800, 800)
                                # Muestra la imagen y la información DICOM actualizada
                                window_imagen_dicom["-IMAGE-"].update(data=img_resized)
                                window_imagen_dicom["-INFO-"].update(value=info_dicom)
                                window_imagen_dicom["-FILENAME-"].update(value=archivos_dicom[indice_actual])
                            else:
                                sg.popup_error("Error al abrir el archivo DICOM.")

                        elif event_imagen == "-BUTTON-":
                            
                            # Implementar la búsqueda
                            valor_busqueda = values_imagen.get("-SEARCH-", "")
                            filtro_seleccionado = values_imagen.get("-FILTER-", "")
                            if valor_busqueda and filtro_seleccionado:
                                resultados = filtrar_datos_dicom(ds, filtro_seleccionado, valor_busqueda)
                                filtrados = "\n".join([str(elem) for elem in resultados])
                                
                                layout_filtro_dicom = [
                                                [sg.Multiline(key="-INFO-", size=(50, 20), expand_x=True, expand_y=True, disabled=True )],
                                            ]

                                window_filtro_dicom = sg.Window(
                                    "Filtro DICOM", 
                                    layout_filtro_dicom, 
                                    finalize=True, 
                                    resizable=True, 
                                    size=(800, 300)  # Tamaño inicial de la ventana
                                )
                               
                                window_filtro_dicom["-INFO-"].update(value=filtrados)
                            else:
                                sg.popup("No se encontraron resultados para la búsqueda.")
                            
                    window_imagen_dicom.close()
            else:
                sg.popup_error("No se encontraron archivos DICOM en la carpeta seleccionada.")


# Cierra la ventana principal al salir del bucle
window.close()
