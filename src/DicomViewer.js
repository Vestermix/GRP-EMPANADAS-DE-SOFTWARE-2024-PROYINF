import React, { useEffect, useRef } from 'react';
import cornerstone from 'cornerstone-core';
import cornerstoneWADOImageLoader from 'cornerstone-wado-image-loader';

cornerstoneWADOImageLoader.external.cornerstone = cornerstone;
cornerstoneWADOImageLoader.configure({
    useWebWorkers: true,
});

// Componente para la visualización de imágenes DICOM
const DicomViewer = ({ dicomImage }) => {
    const imageElementRef = useRef(null);

    useEffect(() => {
        if (dicomImage && imageElementRef.current) {
            const imageElement = imageElementRef.current;
            cornerstone.enable(imageElement); // Habilitar el visualizador de cornerstone en este elemento
            console.log('Contenedor habilitado:', imageElement);
            cornerstone.displayImage(imageElement, dicomImage); // Mostrar la imagen DICOM
        }
    }, [dicomImage]); // Solo se actualiza cuando dicomImage cambia

    return (
        <div
            ref={imageElementRef}
            style={{
                width: '100%',
                height: '500px',
                backgroundColor: 'lightgray',
                border: '2px solid black',
            }}
        ></div>
    );
};

export default DicomViewer;
