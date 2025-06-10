import axios from 'axios';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8001';

const api = axios.create({
  baseURL: `${API_URL}/api/v1`,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Serviços de Audiobook - SEM AUTENTICAÇÃO
export const audioBookService = {
  // Upload de arquivo para criar audiobook
  uploadFile: async (file) => {
    const formData = new FormData();
    formData.append('file', file);
    
    const response = await axios.post(`${API_URL}/api/v1/audiobooks/`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data;
  },

  // Criar audiobook a partir de texto direto
  createFromText: async (title, text) => {
    const formData = new FormData();
    formData.append('title', title);
    formData.append('text', text);
    
    const response = await axios.post(`${API_URL}/api/v1/audiobooks/from-text`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data;
  },

  // Listar audiobooks
  getAudiobooks: async () => {
    const response = await api.get('/audiobooks/');
    return response.data;
  },

  // Obter detalhes de um audiobook
  getAudiobook: async (id) => {
    const response = await api.get(`/audiobooks/${id}`);
    return response.data;
  },

  // Verificar status do processamento
  getAudiobookStatus: async (id) => {
    const response = await api.get(`/audiobooks/${id}/status`);
    return response.data;
  },

  // Deletar audiobook
  deleteAudiobook: async (id) => {
    const response = await api.delete(`/audiobooks/${id}`);
    return response.data;
  },
};

export default api; 