import { defineStore } from 'pinia';
import { ref } from 'vue';

export interface Patient {
    id: number;
    first_name: string;
    last_name: string;
    email: string;
    has_test: boolean;
    gender: string;
    age: string;
    skin_type?: string;
    role: string;
    password?: string;
    experience_age?: string;
    speciality?: string;
    university?: string;
}
export interface Folder {
    id: number;
    folder_name: string;
    body_part: string;
    created_at: string;
}
export interface Doctor {
    id: number;
    email: string;
    first_name: string;
    last_name: string;
    gender: string;
    password?: string;
    experience_age: string;
    speciality: string;
    university: string;
    age: string;
    role: string;
    skin_type?: string;
    has_test: boolean;
}

// Объявляем Pinia-хранилище для хранения данных пользователя
export const useUserStore = defineStore('user', () => {
    // Используем объединение типов для user, чтобы хранить как Doctor, так и Patient
    const user = ref<Patient | Doctor | null>(null);

    // Метод для установки пользователя
    const setUser = (newUser: Patient | Doctor) => {
        user.value = newUser;
    };

    // Метод для очистки данных пользователя
    const clearUser = () => {
        user.value = null;
    };

    return { user, setUser, clearUser };
});
