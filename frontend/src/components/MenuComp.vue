<template>
    <nav class="menu" :style="role.role === 'doctor' ? 'gap: 53px; justify-content: center' : ''">
        <CustomMenuLink :to="`/doctor/chats`" icon="docChats" text="Пациенты" v-if="role.role === 'doctor'" />
        <CustomMenuLink :to="`/patient/home`" icon="home" text="Главная" v-if="role.role === 'patient'" />
        <CustomMenuLink :to="`/patient/history`" icon="scan" text="История" v-if="role.role === 'patient'" />
        <CustomIcon id="camera" :width="52" :height="52" @click="router.push('/camera')" />
        <CustomMenuLink :to="`/ai_chat`" icon="chat" text="АI-чат" />
        <CustomMenuLink :to="`/patient/chats`" icon="doctor" text="Доктор" v-if="role.role === 'patient'" />
    </nav>
</template>

<script setup lang="ts">
import { useRoleStore } from '@/store/useRoleStore';
import CustomIcon from '@/ui/CustomIcon.vue';
import CustomMenuLink from '@/ui/CustomMenuLink.vue';
import { useRouter } from 'vue-router';

// Get the role store
const role = useRoleStore();
const router = useRouter();
</script>

<style lang="scss">
.menu {
    width: 100%;

    position: fixed;
    bottom: 0;
    left: 0;
    z-index: 2;
    background-color: #ffffff;
    display: flex;
    flex-direction: row;
    justify-content: space-between;
    padding: 10px 20px;
    animation: fadeIn 0.5s ease-in-out forwards;
}
@keyframes fadeIn {
    from {
        opacity: 0;
    }
    to {
        opacity: 1;
    }
}
</style>
