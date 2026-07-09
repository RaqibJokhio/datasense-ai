import axios from 'axios';

const API_BASE_URL = 'https://datasense-ai-p92j.onrender.com/api';

export const uploadFile = async (file) => {
  const formData = new FormData();
  formData.append('file', file);

  const response = await axios.post(`${API_BASE_URL}/upload`, formData, {
    headers: { 'Content-Type': 'multipart/form-data' },
  });
  return response.data;
};

export const queryData = async (sessionId, question) => {
  const response = await axios.post(
    `${API_BASE_URL}/query`,
    { session_id: sessionId, question: question },
    { timeout: 30000 }
  );
  return response.data;
};

export const getAnomalies = async (sessionId) => {
  const response = await axios.get(`${API_BASE_URL}/anomalies/${sessionId}`);
  return response.data;
};

export const downloadAnomaliesCsv = async (sessionId, column) => {
  const response = await axios.get(`${API_BASE_URL}/anomalies/${sessionId}/download`, {
    params: { column },
    responseType: 'blob',
  });

  const url = window.URL.createObjectURL(new Blob([response.data]));
  const link = document.createElement('a');
  link.href = url;
  link.setAttribute('download', `anomalies_${column}.csv`);
  document.body.appendChild(link);
  link.click();
  link.remove();
  window.URL.revokeObjectURL(url);
};