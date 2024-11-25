<template>
    <p class="indikator">{{ step }}/7</p>
    <div class="testPage">
        <TestStep1 v-if="step === 1" v-model:task1="formData.task1" @next-step="handleNextStep" />
        <TestStep2 v-if="step === 2" v-model:task2="formData.task2" @next-step="handleNextStep" @prev-step="handlePrevStep" />
        <TestStep3 v-if="step === 3" v-model:task3="formData.task3" @next-step="handleNextStep" @prev-step="handlePrevStep" />
        <TestStep4 v-if="step === 4" v-model:task4="formData.task4" @next-step="handleNextStep" @prev-step="handlePrevStep" />
        <TestStep5 v-if="step === 5" v-model:task5="formData.task5" @next-step="handleNextStep" @prev-step="handlePrevStep" />
        <TestStep6 v-if="step === 6" v-model:task6="formData.task6" @next-step="handleNextStep" @prev-step="handlePrevStep" />
        <TestStep7 v-if="step === 7" v-model:task7="formData.task7" @next-step="handleNextStep" @prev-step="handlePrevStep" />
        <TestStep8 v-if="step === 8" @submit="handleTestSubmit" />
    </div>
    <p v-if="errorTxt" style="color: red">{{ errorTxt }}</p>
</template>

<script setup lang="ts">
import { ref } from 'vue';

import api from '@/axios/api';
import TestStep1 from './TestSteps/TestStep1.vue';
import TestStep2 from './TestSteps/TestStep2.vue';
import TestStep3 from './TestSteps/TestStep3.vue';
import TestStep4 from './TestSteps/TestStep4.vue';
import TestStep5 from './TestSteps/TestStep5.vue';
import TestStep6 from './TestSteps/TestStep6.vue';
import TestStep7 from './TestSteps/TestStep7.vue';
import TestStep8 from './TestSteps/TestStep8.vue';

const step = ref<number>(1);
const postResponse = ref<PostResponse | null>(null);
const errorTxt = ref<string | null>(null);
const formData = ref<PostData>({
    task1: '',
    task2: '',
    task3: '',
    task4: '',
    task5: '',
    task6: '',
    task7: '',
});

function handleNextStep() {
    if (step.value < 8) {
        step.value++;
    }
}
interface PostData {
    task1: string;
    task2: string;
    task3: string;
    task4: string;
    task5: string;
    task6: string;
    task7: string;
}
interface PostResponse {
    access_token: string;
    token_type: string;
}
const handleTestSubmit = async () => {
    try {
        const response = await api.postData<PostData, PostResponse>('/user/test', formData.value);
        postResponse.value = response;
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
function handlePrevStep() {
    if (step.value > 1) {
        step.value--;
    }
}
</script>

<style lang="scss">
.indikator {
    position: absolute;
    top: 13.51vh;
    left: 20px;
    color: var(--color-main, #418af9);
    font-family: var(--font-main);
    font-size: 16px;
    font-style: normal;
    font-weight: 700;
    line-height: normal;
}
.testPage {
    margin-top: 10.79vh;
    width: 100%;
    padding: 0 20px;
}
</style>
