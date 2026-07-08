import axios from 'axios';

const API_BASE_URL = 'http://127.0.0.1:8000/api';

export const uploadFile = async (file) => {
  const formData = new FormData();
  formData.append('file', file);

  const response = await axios.post(`${API_BASE_URL}/upload`, formData, {
    headers: { 'Content-Type': 'multipart/form-data' },
  });
  return response.data;
};

export const queryData = async (sessionId, question) => {
  const response = await axios.post(`${API_BASE_URL}/query`, {
    session_id: sessionId,
    question: question,
  });
  return response.data;
};

export const getAnomalies = async (sessionId) => {
  const response = await axios.get(`${API_BASE_URL}/anomalies/${sessionId}`);
  return response.data;
};