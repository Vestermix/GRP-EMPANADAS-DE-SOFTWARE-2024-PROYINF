import React, { useState } from 'react';
import { uploadDicom } from './Api'; // Mantén la función de carga de archivos
import DicomViewer from './DicomViewer';  // Importamos el componente DicomViewer
import cornerstone from 'cornerstone-core';

function DicomUploader() {
    const [file, setFile] = useState(null);
    const [metadata, setMetadata] = useState(null);
    const [dicomImage, setDicomImage] = useState(null);
    const [contrast, setContrast] = useState(1);  // Contraste inicial
    const [brightness, setBrightness] = useState(1); // Brillo inicial

    const handleFileChange = (event) => {
        setFile(event.target.files[0]);
    };

    const handleUpload = async () => {
        try {
            const response = await uploadDicom(file);
            setMetadata(response.data.metadata); // Suponiendo que los metadatos se devuelven aquí
            
            const dicomImageUrl = response.data.imageUrl; // Asegúrate de que esta URL sea correcta
            console.log('URL de la imagen:', dicomImageUrl); 
            if (!dicomImageUrl) {
              throw new Error('No se recibió una URL de la imagen.');
            }
            // Cargar la imagen DICOM usando cornerstone.js
            const dicomImage = await cornerstone.loadImage(response.data.imageUrl); // Aquí deberías recibir la URL de la imagen DICOM desde el backend
            console.log('Imagen cargada:', dicomImage);
            setDicomImage(dicomImage);
        } catch (error) {
            console.error('Error al subir el archivo:', error);
        }
    };

    // Función para manejar el ajuste del contraste
    const handleContrastChange = (event) => {
        const newContrast = parseFloat(event.target.value);
        setContrast(newContrast);
        adjustImage();
    };

    // Función para manejar el ajuste del brillo
    const handleBrightnessChange = (event) => {
        const newBrightness = parseFloat(event.target.value);
        setBrightness(newBrightness);
        adjustImage();
    };

    // Función para ajustar el contraste y brillo de la imagen
    const adjustImage = () => {
        if (dicomImage) {
            const newImage = { ...dicomImage }; // Crear una nueva copia de la imagen
            // Aquí puedes agregar lógica para modificar los datos de píxeles
            // Ejemplo simple para ajustar el contraste y el brillo (esto puede requerir personalización)
            newImage.windowWidth = contrast * 1000;
            newImage.windowCenter = brightness * 500;

            // Actualizar el estado de la imagen
            setDicomImage(newImage);
        }
    };

    return (
        <div>
            <h1>Subir Imagen DICOM</h1>
            <input type="file" accept=".dcm" onChange={handleFileChange} />
            <button onClick={handleUpload}>Subir</button>

            {metadata && (
                <div>
                    <h3>Metadatos:</h3>
                    <pre>{JSON.stringify(metadata, null, 2)}</pre>
                </div>
            )}

            <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                {/* Contenedor para el visualizador de la imagen */}
                {dicomImage && <DicomViewer dicomImage={dicomImage} />}

                {/* Contenedor para los controles de ajuste */}
                {dicomImage && (
                    <div style={{ width: '35%', padding: '10px' }}>
                        <h3>Ajustes de Imagen</h3>
                        <div>
                            <label>Contraste</label>
                            <input
                                type="range"
                                min="0"
                                max="2"
                                step="0.1"
                                value={contrast}
                                onChange={handleContrastChange}
                            />
                        </div>
                        <div>
                            <label>Brillo</label>
                            <input
                                type="range"
                                min="0"
                                max="2"
                                step="0.1"
                                value={brightness}
                                onChange={handleBrightnessChange}
                            />
                        </div>
                    </div>
                )}
            </div>
        </div>
    );
}

export default DicomUploader;
