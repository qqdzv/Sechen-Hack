// src/stores/useRoleStore.ts
import { defineStore } from 'pinia';
import { ref } from 'vue';
import { useUserStore } from './useUserStore';
export interface Scan {
    id:number;
    folder_id:number;
    response:string;
    percent:number;
    type:string;
    result:string;
    recommendations:string;
    image_base64:string;
    created_at:string;
}
// Обновленный интерфейс Folder
export interface Folder {
    id: number;
    folder_name: string;
    body_part: string;
    created_at: string;
    scans?: Scan[]; // Добавлено поле для сканов
}
export const useScansStore = defineStore('scan', () => {
    // Define the role state
    const folders = ref<Folder[]>([]);
    const scans = ref<Scan[]>([]);
    const userStore = useUserStore();
    // Define actions to set and clear the role
    const setFolders = (newFolders: Folder[]) => {
        if (userStore.user && userStore.user.role === 'user') {
            folders.value = newFolders;
        } else {
            console.warn("Роль пользователя не 'user' или `user` не задан");
        }
    };
    const getFolders = () => {
        if (folders.value) {
            return folders.value;
        }
    };
    const getAllScans = () => {
        if (scans.value) {
            return scans.value;
        }
    };
    const setAllScans = (newScans: Scan[]) => {
        scans.value = newScans;
    };
    return {scans, folders, setFolders, getFolders, getAllScans, setAllScans };
});
