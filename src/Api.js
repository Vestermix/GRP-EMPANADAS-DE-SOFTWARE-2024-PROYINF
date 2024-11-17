import axios from 'axios';

const api = axios.create({
    baseURL: 'http://localhost:8000/dicom/', // Base URL del backend Django
});

export const uploadDicom = (file) => {
    const formData = new FormData();
    formData.append('file', file);

    return api.post('upload/', formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
    });
};

export default api;
