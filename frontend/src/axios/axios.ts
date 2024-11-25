import { getCookie } from '@/utils/getCookie';
import axios from 'axios';

// Create an Axios instance
const axiosInstance = axios.create({
    baseURL: import.meta.env.VITE_API_URL, // Replace with your API base URL
    timeout: 20000, // Optional: set a timeout for requests
    headers: {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*',
        // You can add more custom headers here if needed
    },
});

// Request Interceptor
axiosInstance.interceptors.request.use(
    (config) => {
        // Add authorization token or modify the config if needed
        const token = getCookie('token');
        if (token) {
            config.headers.Authorization = `Bearer ${token}`;
        }
        return config;
    },
    (error) => {
        // Handle the error
        return Promise.reject(error);
    },
);

// Response Interceptor
axiosInstance.interceptors.response.use(
    (response) => {
        // Handle the response data if needed
        return response;
    },
    (error) => {
        // Handle the error response
        console.error('Response error:', error);
        return Promise.reject(error);
    },
);

export default axiosInstance;
