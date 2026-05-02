import axios from 'axios';

const api = axios.create({
  baseURL: 'http://127.0.0.1:8000',
  headers: {
    'Content-Type': 'application/json',
  },
});

export const planTrip = async (data) => {
  try {
    const response = await api.post('/plan-trip', data);
    return response.data;
  } catch (error) {
    console.error('Error planning trip:', error);
    throw error;
  }
};
