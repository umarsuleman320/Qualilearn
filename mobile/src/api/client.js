import axios from 'axios';

// The laptop's local IP address for mobile-to-backend communication
export const BASE_URL = 'http://192.168.117.253:8000/api/v1';

const apiClient = axios.create({
  baseURL: BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export default apiClient;
