<template>
    <p class="indikator">{{ step }}/8</p>
    <div class="regPage">
        <RegStep1 v-if="step === 1" v-model:name="formData.first_name" v-model:surname="formData.last_name" @next-step="handleNextStep" />
        <RegStep2 v-if="step === 2" v-model:email="formData.email" @next-step="handleNextStep" @prev-step="handlePrevStep" />
        <RegStep3 v-if="step === 3" v-model:password="formData.password" @next-step="handleNextStep" @prev-step="handlePrevStep" />
        <RegStep4 v-if="step === 4" v-model:gender="formData.gender" @next-step="handleNextStep" @prev-step="handlePrevStep" />
        <RegStep5 v-if="step === 5" v-model:age="formData.age" @next-step="handleNextStep" @prev-step="handlePrevStep" />
        <RegStep6 v-if="step === 6" v-model:experience="formData.experience_age" @next-step="handleNextStep" @prev-step="handlePrevStep" />
        <RegStep7 v-if="step === 7" v-model:university="formData.university" @next-step="handleNextStep" @prev-step="handlePrevStep" />
        <RegStep8 v-if="step === 8" v-model:speciality="formData.speciality" @submit="handleRegister" @prev-step="handlePrevStep" />
    </div>
    <p style="color: red; font-family:var(--font-main)">{{ errorTxt }}</p>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue';
import RegStep1 from './RegSteps/RegDocStep1.vue';
import RegStep2 from './RegSteps/RegDocStep2.vue';
import RegStep3 from './RegSteps/RegDocStep3.vue';
import RegStep4 from './RegSteps/RegDocStep4.vue';
import RegStep5 from './RegSteps/RegDocStep5.vue';
import RegStep6 from './RegSteps/RegDocStep6.vue';
import RegStep7 from './RegSteps/RegDocStep7.vue';
import RegStep8 from './RegSteps/RegDocStep8.vue';
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
    experience_age: '',
    speciality: '',
    university: '',
    age: '',
    role: 'doctor',
});

function handleNextStep() {
    if (step.value < 8) {
        step.value++;
    }
}
interface PostData {
    email: string;
    first_name: string;
    last_name: string;
    gender: string;
    password: string;
    experience_age: string;
    speciality: string;
    university: string;
    age: string;
    role: string;
}
interface PostResponse {
    access_token: string;
    token_type: string;
}
const handleRegister = async () => {
    try {
        const response = await api.postData<PostData, PostResponse>('/doctor/register', formData.value);
        postResponse.value = response;
        setTimeout(() => {
            router.push('/doctor/chats');
        }, 1000);
    } catch (error: any) {
        // Проверяем структуру ошибки, чтобы получить нужное сообщение
        if (error.response?.data?.detail) {
            // Если `detail` — это массив, берем первое сообщение
            if (Array.isArray(error.response.data.detail) && error.response.data.detail.length > 0) {
                errorTxt.value = error.response.data.detail[0].msg || 'Неизвестная ошибка';
            } else {
                errorTxt.value = error.response.data.detail;
            }
        } else if (error.response?.data?.message) {
            errorTxt.value = error.response.data.message;
        } else {
            errorTxt.value = 'Произошла ошибка, попробуйте еще раз позже';
        }
        console.log(errorTxt.value);
    }
};

watch(postResponse, (newPostResponse) => {
    if (newPostResponse && newPostResponse.access_token) {
        setCookie('token', newPostResponse.access_token, 4);
    } else {
        console.error('Access token is undefined');
    }
});
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
