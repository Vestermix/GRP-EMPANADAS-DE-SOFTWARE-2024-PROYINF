Este es el repositorio del grupo "Empanadas de Software", cuyos integrantes son:

# Grupo Empanadas de Software
(Actualizado semestre 2024 - 2)
* Geraldine Cornejo - 202173529-1
* Alonso Diaz - 202173602-6
* Javiera Barrales - 202173536-4
* Andrea Delgadillo - 202490508-2


## WIKI
* (Para revisar trabajos del semestre 2024 - 2 visitar Wiki)
* [Wiki grupo empanadas de software](https://github.com/Vestermix/GRP-EMPANADAS-DE-SOFTWARE-2024-PROYINF/wiki)

## Instrucciones de uso para la interfaz 
(Todo funciona con enlaces en botones, por lo que es importante que no se desplace a lo largo del archivo sin ser direccionado por un botón)
* Primero, como es un archivo pdf, este debe descargarse y la página se debe ajustar de acuerdo al tamaño de la pantalla.
* Luego, se simula cómo la aplicación es capaz de cargar una carpeta. Cuando se hace click en seleccionar carpeta, esta lleva a la visualización de las imágenes donde hay botones para moverse entre imágenes y un botón para ir al buscador DICOM.
* En el buscador DICOM dejamos unos ejemplos de su funcionamiento, donde si se aprieta en el tipo de filtro saldrá una búsqueda y luego se debe apretar en la lupa para hacer la búsqueda. Esta página cuenta con dos botones extras: uno que es para reestablecer la búsqueda (flecha girando), donde se borran los filtros, y otro donde se puede volver a la visualización de imágenes (casita).

## Video Explicativo
* Video explicando el prototipo - Hito 4 -
https://youtu.be/BRtxL4Nvu2Q
* Archivo VisualizadorDicom.py, se encuentra en carpeta funcionalidadesBase, es el único archivo python a utilizar en esta entrega
* Paso_a_paso_creacion_proyecto.txt es un archivo donde se explica la creación del entorno de proyecto
## HITO 5
* LINK A VIDEO: https://youtu.be/P2pTEBZrhxI

# Trabajo semestre 2024 - 2
Proyecto base: El semestre pasado se trabajo en base a una característica requerida por el cliente, la cual es: Mostrar información de la cabecera DICOM e incorporar un buscador.
Este semestre se buscará finalizar el buscador y pulir el trabajo con lo aprendido en clases.
## Hito 4
Actualizaciones en código: Se implementaron los requerimientos en cuanto al procesamiento de imágenes Dicom, sin embargo, se nos hizo imposible integrarlo con lo que tenemos en Django (registro y login), lo cual quedará para la siguiente entrega.
Estos archivos nuevos están en 'ArchivosProyectoDjango/dwv', el cual cuenta con varios zip, para poder ejecutar el visualizador se deben descomprimir todas las carpetas y ejecutar los comandos a continuación en consola.

```bash
# Desde la carpeta donde estará el Proyecto General, moverse al visualizador
cd dwv

# instalar las dependencias
yarn install

# ejecutar proyecto: abre una página automáticamente
yarn run start
```

