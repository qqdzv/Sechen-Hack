<template>
    <p class="indikator">{{ step }}/6</p>
    <div class="regPage">
        <RegStep1 v-if="step === 1" v-model:name="formData.first_name" v-model:surname="formData.last_name" @next-step="handleNextStep" />
        <RegStep2 v-if="step === 2" v-model:email="formData.email" @next-step="handleNextStep" @prev-step="handlePrevStep" />
        <RegStep3 v-if="step === 3" v-model:password="formData.password" @next-step="handleNextStep" @prev-step="handlePrevStep" />
        <RegStep4 v-if="step === 4" v-model:gender="formData.gender" @next-step="handleNextStep" @prev-step="handlePrevStep" />
        <RegStep5 v-if="step === 5" v-model:age="formData.age" @next-step="handleNextStep" @prev-step="handlePrevStep" />
        <RegStep6 v-if="step === 6" v-model:skinType="formData.skin_type" @prev-step="handlePrevStep" @submit="handleRegister" />
    </div>
    <p style="color: red; font-family:var(--font-main)">{{ errorTxt }}</p>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue';
import RegStep1 from './RegSteps/RegStep1.vue';
import RegStep2 from './RegSteps/RegStep2.vue';
import RegStep3 from './RegSteps/RegStep3.vue';
import RegStep4 from './RegSteps/RegStep4.vue';
import RegStep5 from './RegSteps/RegStep5.vue';
import RegStep6 from './RegSteps/RegStep6.vue';
import { useRouter } from 'vue-router';
import api from '@/axios/api';
import { setCookie } from '@/utils/setCookie';

const router = useRouter();
const step = ref<number>(1);
const postResponse = ref<PostResponse | null>(null);
const errorTxt = ref<string | null>(null);
const formData = ref<PostData>({
    email: '',
    first_name: '',
    last_name: '',
    gender: '' as 'male' | 'female',
    password: '',
    skin_type: '',
    age: '',
    role: 'user',
});

function handleNextStep() {
    if (step.value < 6) {
        step.value++;
    }
}
interface PostData {
    email: string;
    first_name: string;
    last_name: string;
    gender: string;
    password: string;
    skin_type: string;
    age: string;
    role: string;
}
interface PostResponse {
    access_token: string;
    token_type: string;
}
watch(postResponse, (newPostResponse) => {
    if (newPostResponse && newPostResponse.access_token) {
        setCookie('token', newPostResponse.access_token, 4);
    } else {
        console.error('Access token is undefined');
    }
});
const handleRegister = async () => {
    try {
        const response = await api.postData<PostData, PostResponse>('/user/register', formData.value);
        postResponse.value = response; // Для отладки
        setTimeout(() => {
            router.push('/patient/home');
        }, 1000);
    } catch (error: any) {
        console.log(error.response.data.message);
        errorTxt.value = error.response.data.detail;
    }
};

function handlePrevStep() {
    if (step.value > 1) {
        step.value--;
    }
}
</script>

<style lang="scss">
.indikator {
    position: absolute;
    top: 29.51vh;
    left: 20px;
    color: var(--color-main, #418af9);
    font-family: var(--font-main);
    font-size: 16px;
    font-style: normal;
    font-weight: 700;
    line-height: normal;
}
.regPage {
    margin-top: 28.79vh;
    width: 100%;
    padding: 0 20px;
}
</style>
