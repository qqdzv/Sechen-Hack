<template>
    <div class="globalAuth">
        <div class="step4">
            <h2>Выбери свою роль</h2>
            <div class="groupBtns">
                <MainButton text="Врач" :key="roleStore.role === 'doctor' ? 'doctor-button' : 'base-doctor'" @click="selectRole('doctor')" :type="roleStore.role === 'doctor' ? 'primary' : 'base'" :width="165" />
                <MainButton text="Пациент" @click="selectRole('patient')" :key="roleStore.role === 'patient' ? 'patient-button' : 'base-patient'" :type="roleStore.role === 'patient' ? 'primary' : 'base'" :width="165" />
            </div>
        </div>
        <div class="bottom">
            <MainButton text="Далее" @click="nextStep" type="primary" />
        </div>
    </div>
</template>

<script setup lang="ts">
import { useRoleStore } from '@/store/useRoleStore.ts';
import { useRouter } from 'vue-router';
import MainButton from '@/ui/MainButton.vue';
import { getCookie } from '@/utils/getCookie';

// Access the store
const roleStore = useRoleStore();
const router = useRouter();

// Set the selected role
const selectRole = (role: string) => {
    roleStore.setRole(role);
    console.log(roleStore.role);
};

// Navigate to the next step
const nextStep = () => {
    if (roleStore.role) {
        if (getCookie('token')) {
            if (roleStore.role === 'patient') {
                router.push('/patient/home');
            } else {
                router.push('/doctor/chats');
            }
        }
        else {
            router.push('/login/' + roleStore.role);
        }
    }
    
};
</script>

<style lang="scss" scoped>
.globalAuth {
    margin-top: 28.79vh;
    width: 100%;
    padding: 0 20px;
    .step4 {
        display: flex;
        flex-direction: column;
        gap: 68px;
        width: 100%;
        height: 100%;
        .groupBtns {
            display: flex;
            flex-direction: row;
            width: 100%;
            justify-content: space-between;
        }
        h2 {
            color: var(--Text, #1d1d1d);
            font-family: var(--font-main);
            font-size: 32px;
            font-style: normal;
            font-weight: 600;
            line-height: normal;
        }
    }
    .bottom {
        position: fixed;
        width: 89.7435897vw;
        bottom: 50px;
        display: flex;
        flex-direction: row;
        justify-content: flex-end;
    }
}
</style>
