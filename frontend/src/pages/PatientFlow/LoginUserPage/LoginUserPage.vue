<template>
    <div class="loginPage">
        <LoginStep1 v-if="step === 1" v-model:email="email" @next-step="step = 2" />
        <LoginStep2 v-if="step === 2" v-model:password="password" @prev-step="step = 1" @submit="handleLogin" />
    </div>
    <p style="color: red; font-family:var(--font-main)">{{ errorTxt }}</p>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue';
import LoginStep1 from './LoginSteps/LoginStep1.vue';
import LoginStep2 from './LoginSteps/LoginStep2.vue';
import api from '@/axios/api';
import { useRouter } from 'vue-router';
import { setCookie } from '@/utils/setCookie';

interface PostData {
    email: string;
    password: string;
}

interface PostResponse {
    access_token: string;
    token_type: string;
}
const router = useRouter();
const step = ref(1);
const email = ref(''); // значение email будет передаваться из LoginStep1
const password = ref(''); // значение password будет передаваться из LoginStep2
const postResponse = ref<PostResponse | null>(null);
const errorTxt = ref<string | null>(null);
watch(postResponse, (newPostResponse) => {
    if (newPostResponse && newPostResponse.access_token) {
        setCookie('token', newPostResponse.access_token, 4);
    } else {
        console.error('Access token is undefined');
    }
});

watch(errorTxt, (newError) => {
    if (newError?.includes('422')) {
        errorTxt.value = 'Некоректный логин или пароль';
    }
    if (newError?.includes('400')) {
        errorTxt.value = 'Неверный логин или пароль';
    }
});
const handleLogin = async () => {
    try {
        const response = await api.postData<PostData, PostResponse>('/user/login', { email: email.value, password: password.value });
        postResponse.value = response; // Устанавливаем значение postResponse
        router.push('/patient/home');
    } catch (error: any) {
        errorTxt.value = error.response.data.detail;
        console.log(error.response.data.message);
    }
};
</script>
<style lang="scss">
.loginPage {
    margin-top: 50%;
    width: 100%;
    padding: 0 20px;
}
</style>
