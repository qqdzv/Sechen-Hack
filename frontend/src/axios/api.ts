import axiosInstance from './axios'; // Import the configured Axios instance

// Define API methods
const api = {
    async getData<T>(endpoint: string): Promise<T> {
        try {
            const response = await axiosInstance.get<T>(endpoint);
            return response?.data; // Return the fetched data (response.data)
        } catch (error) {
            console.error('Error fetching data:', error);
            throw error; // Re-throw the error for handling in the component
        }
    },
    async postData<T, R>(endpoint: string, data: T): Promise<R> {
        try {
            const response = await axiosInstance.post<R>(endpoint, data);
            return response?.data; // Вернуть только данные ответа
        } catch (error) {
            console.error('Error posting data:', error);
            throw error; // Пробрасываем ошибку для обработки в компоненте
        }
    },
};

export default api;
