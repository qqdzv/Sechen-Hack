<template>
    <main class="testLayout" v-if="optionSelected === null">
        <div class="testPage">
            <h3>
                Хотите поиграть <br />
                в игру пока ждете результат?
            </h3>
            <div class="twoBtn">
                <button :class="['btn', optionSelected === 'Нет' ? 'active' : '']" :key="optionSelected === 'Нет' ? 'male-button' : 'base-male'" @click="optionSelected = 'Нет'">Нет</button>
                <button :class="['btn', optionSelected === 'Да' ? 'active' : '']" :ket="optionSelected === 'Да' ? 'male-button' : 'base-male'" @click="optionSelected = 'Да'">Да</button>
            </div>
        </div>
    </main>
    <main class="testLayout" v-if="optionSelected === 'Нет'">
        <ScanLoading @load-analys="handleLoadAnalys" />
    </main>
    <main class="testLayout" v-if="optionSelected === 'Да'">
        <QuizLoadHeader @load-analys="handleLoadAnalys" />
        <QuizStep1 v-if="step === 1" @next-step="handleNextStep" :step="step" />
        <QuizStep2 v-if="step === 2" @prev-step="handlePrevStep" :step="step" />
    </main>
    <div class="modal_overlay" v-if="openModal" @click="closeModal"></div>
    <div class="modal" v-if="openModal">
        <p style="color: red">{{ errorTxt }}</p>
        <MainButton text="Пройти заново" @click="router.back()" type="secondary" />
    </div>
</template>

<script setup lang="ts">
defineOptions({
    name: 'QuizPage',
});
import { computed, nextTick, onMounted, ref, toRaw, watch } from 'vue';
import CustomIcon from '@/ui/CustomIcon.vue';
import { useRouter, useRoute } from 'vue-router';
import QuizStep1 from './QuizSteps/QuizStep1.vue';
import QuizStep2 from './QuizSteps/QuizStep2.vue';
import { useUserStore } from '@/store/useUserStore';
import api from '@/axios/api';
import MainButton from '@/ui/MainButton.vue';
import ScanLoading from './ScanLoading.vue';

import QuizLoadHeader from './QuizLoadHeader.vue';

interface PostData {
    gender: string;
    age: string;
    body_part: string | null;
    folder_name: string;
    size: string | null;
    how_many_days: string | null;
    have_pain: boolean;
    have_medicines: boolean;
    mixing: string | null;
    image_base64: string;
}
interface PostData2 {
    gender: string;
    age: string;
    body_part: string | null;
    folder_name: string;
    size: string | null;
    how_many_days: string | null;
    have_pain: boolean;
    have_medicines: boolean;
    mixing: string | null;
    image_base64: string;
}
interface PostResponse {
    id: number;
    response: string;
    percent: number;
    type: string;
    result: string;
    recommendations: string;
    image_base64: string;
}

const step = ref<number>(1);
const optionSelected = ref<string | null>(null);
const errorTxt = ref<string | null>(null);
const router = useRouter();
const route = useRoute();
const postResponse = ref<PostResponse | null>(null);
const userStore = useUserStore();
const openModal = ref<boolean>(false);
const formData = ref<PostData | null>(null);

watch(errorTxt, (newError) => {
    if (newError) {
        openModal.value = true;
    }
});
onMounted(() => {
    const queryFormData = route.query.formData;

    // Проверяем, что queryFormData не null, а затем преобразуем строку JSON в объект
    if (typeof queryFormData === 'string') {
        try {
            formData.value = JSON.parse(queryFormData) as PostData;
            console.log(formData.value);
        } catch (error) {
            console.error('Ошибка при парсинге formData:', error);
        }
        handleSendForm();
        router.replace({ path: route.path });
    } else {
        console.log('formData is null');
        router.replace('/temp-route').then(() => {
            router.replace('/camera');
        });
    }
});
function closeModal() {
    openModal.value = false;
}
function handleNextStep() {
    if (step.value < 2) {
        step.value++;
    }
}
function handlePrevStep() {
    if (step.value > 1) {
        step.value--;
    }
}
function handleLoadAnalys() {
    if(postResponse.value){
        router.push({ path: '/scanReport', query: { scanID: postResponse.value?.id } });
    }

}
const handleSendForm = async () => {
    if (userStore.user?.role === 'user' && formData.value) {
        if (!formData.value.body_part) {
            formData.value.body_part = "head/neck";
            formData.value.size = '3333';
            formData.value.how_many_days = 'sad';
            formData.value.have_pain = false;
            formData.value.have_medicines = false;
            formData.value.mixing = 'string';
        }
        try {
            const response = await api.postData<PostData, PostResponse>('/scan/send_new', formData.value);
            if (response) {
                setTimeout(() => {
                    postResponse.value = response;
                }, 1000);
            }
        } catch (error: any) {
            errorTxt.value = error.response.data.detail
        }
    } else {
        if (formData.value) {
            try {
                const formData2 = ref<PostData2>({
                    have_medicines: false,
                    have_pain: false,
                    gender: formData.value.gender,
                    age: formData.value.age,
                    body_part: formData.value.body_part,
                    image_base64: formData.value.image_base64,
                    folder_name: "dsa",
                    how_many_days: "sdadsad",
                    mixing: "sadsa",
                    size: null
                });
                console.log(formData2.value);

                const response = await api.postData<PostData2, PostResponse>('/doctor/send_new', formData2.value);
                postResponse.value = response;
            } catch (error: any) {
                if (error.response?.data?.detail) {
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
        }
    }
};
</script>

<style lang="scss" scoped>
.testLayout {
    width: 100%;

    display: flex;
    flex-direction: column;
    align-items: center;
    height: 100dvh;
    background-color: var(--color-main);
    padding: 16px 20px;
    gap: 16px;
}

.testPage {
    padding-top: 20px;
    width: 100%;
    height: 100%;
    h3 {
        color: var(--Bg, #fafafa);
        /* H2 */
        font-family: var(--font-main);
        font-size: 32px;
        font-style: normal;
        font-weight: 600;
        line-height: normal;
    }
    .twoBtn {
        margin-top: 32px;
        display: flex;
        flex-direction: row;
        justify-content: space-between;
        align-items: center;
        .btn {
            display: flex;
            width: 46%;
            height: 48px;
            padding: 0px 24px;
            justify-content: center;
            align-items: center;
            gap: 8px;
            border-radius: 12px;
            border: 1px solid #efefef;

            color: var(--Bg, #efefef);
            font-family: var(--font-main);
            font-size: 16px;
            font-style: normal;
            font-weight: 700;
            line-height: 24px; /* 150% */
            background: transparent;
        }
        .active {
            background: #fff;
            color: var(--color-main);
        }
    }
}
.modal_overlay {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background-color: rgba(0, 0, 0, 0.5);
    z-index: 5;
}

.modal {
    position: fixed;
    bottom: 50%;
    left: 50%;
    transform: translate(-50%, 50%);
    padding: 20px;
    z-index: 6;
    border-radius: 8px;
    width: 90%;
    font-family: var(--font-main);
    font-weight: 600;
    background-color: #fafafa;
    border-radius: 20px;
}
</style>
