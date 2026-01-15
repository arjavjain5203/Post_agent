import axios from 'axios';

const api = axios.create({
    baseURL: 'http://localhost:8000/api/v1',
    withCredentials: true, // Send cookies with requests
    headers: {
        'Content-Type': 'application/json',
    },
});

// Response interceptor (optional, for 401 handling)
api.interceptors.response.use(
    (response) => response,
    (error) => Promise.reject(error)
);

export default api;
