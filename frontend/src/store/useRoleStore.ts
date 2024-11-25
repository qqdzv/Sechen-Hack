// src/stores/useRoleStore.ts
import { defineStore } from 'pinia';
import { ref } from 'vue';

export const useRoleStore = defineStore('role', () => {
    // Define the role state
    let defineRole = window.location.href.includes('/doctor') ? 'doctor' : 'patient';
    const role = ref<string>(defineRole);

    // Define actions to set and clear the role
    const setRole = (newRole: string) => {
        role.value = newRole;
    };

    const clearRole = () => {
        role.value = '';
    };

    return { role, setRole, clearRole };
});
