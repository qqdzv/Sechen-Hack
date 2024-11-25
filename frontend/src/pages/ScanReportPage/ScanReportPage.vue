<template>
    <main class="reportLayout">
        <div class="reportHeader">
            <div class="circlePhoto" :style="{ borderColor: typeColor }">
                <img v-if="scanReport" :src="scanReport?.image_base64" alt="photo" />
                <div v-else class="skeleton circlePhotoSkeleton"></div>
            </div>
            <div class="resultTexts">
                <h3 v-if="scanReport">{{ scanReport?.percent.toFixed(0) }}%</h3>
                <div v-else class="skeleton resultTextSkeleton"></div>
                <p v-if="scanReport">{{ scanReport && extractTextInParentheses(scanReport?.response) }}</p>
                <div v-else class="skeleton resultTextSkeleton"></div>
            </div>
        </div>
        <div class="conclusion">
            <h4>Вывод</h4>
            <p v-if="scanReport">{{ scanReport?.result }}</p>
            <div v-else class="skeleton conclusionSkeleton"></div>
        </div>
        <div class="btns" v-if="userStore.user?.role !== 'doctor'">
            <MainButton text="Напомнить" @click="setNotification" type="secondary" />
            <MainButton text="Отправить врачу" @click="router.push('/allDoctors')" type="primary" style="width: 100%" />
        </div>
        <div class="recomendations">
            <h4>Рекомендации</h4>
            <p v-if="scanReport">{{ scanReport?.recommendations }}</p>
            <div v-else class="skeleton recommendationsSkeleton"></div>
        </div>
        <div class="modal_overlay" v-if="openModal" @click="closeModal"></div>
        <div class="modal" v-if="openModal">
            <p class="txt">{{ notification }}</p>
            <button @click="closeModal" class="close-btn">Закрыть</button>
        </div>
    </main>
    <MenuComp />
</template>

<script setup lang="ts">
defineOptions({
    name: 'ScanReportPage',
});
import { computed, onMounted, ref } from 'vue';

import { useRouter, useRoute } from 'vue-router';

import MainButton from '@/ui/MainButton.vue';
import MenuComp from '@/components/MenuComp.vue';
import api from '@/axios/api';
import { extractTextInParentheses } from '@/utils/getTxtByRegxp';
import { useUserStore } from '@/store/useUserStore';

interface ScanReport {
    id: number;
    response: string;
    percent: number;
    type: string;
    result: string;
    recommendations: string;
    image_base64: string;
}

const errorTxt = ref<string | null>(null);
const openModal = ref<boolean>(false);
const userStore = useUserStore();
const route = useRoute();
const router = useRouter();
const notification = ref('');
const typeColor = computed(() => {
    return scanReport.value?.type === 'bad' ? '#FFA2A3' : '#A2FFA5';
});
const scanReport = ref<ScanReport | null>(null);
const fetchScanReport = async () => {
    const scanID = route.query.scanID;
    if (scanID) {
        try {
            const response = await api.getData<ScanReport>(`/scan/scan_by_id/${scanID}`);
            if (response) {
                scanReport.value = response;
            }
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
        }
    } else {
        console.log('scanReport is null');
    }
};

const setNotification = async () => {
    try{
        const response = await api.getData<{ detail: string }>('/user/set_notification');
        if (response) {
            notification.value = response?.detail;
        }

    } catch (error: any) {
        if (error.response?.data?.detail) {
            if (Array.isArray(error.response.data.detail) && error.response.data.detail.length > 0) {
                notification.value = error.response.data.detail[0].msg || 'Неизвестная ошибка';
            } else {
                notification.value = error.response.data.detail;
            }
        } else if (error.response?.data?.message) {
            notification.value = error.response.data.message;
        } else {
            notification.value = 'Произошла ошибка, попробуйте еще раз позже';
        }
    }
    finally {
        openModal.value = true;
    }

};
function closeModal() {
    openModal.value = false;
}
onMounted(() => {
    fetchScanReport();
});
</script>

<style lang="scss" scoped>
.reportLayout {
    width: 100%;

    display: flex;
    flex-direction: column;
    align-items: center;
    height: 100vh;
    overflow-y: auto;
    background-color: var(--bg-1);
    padding: 5px 20px;
    gap: 26px;
    font-family: var(--font-main);
    .reportHeader {
        width: 100%;
        display: flex;
        flex-direction: row;
        align-items: center;
        gap: 20px;
        height: 150px;
        .circlePhoto {
            width: 152px;
            height: auto;
            padding: 3px;
            border: 2px solid;
            border-radius: 50%;
            img {
                width: 100%;
                height: auto;
                border-radius: 50%;
            }
        }
        .resultTexts {
            h3 {
                color: var(--Main, #418af9);
                font-family: var(--font-main);
                font-size: 48px;
                font-style: normal;
                font-weight: 700;
                line-height: normal;
                width: fit-content;
            }
            p {
                width: fit-content;
                color: var(--Text, #1d1d1d);
                font-family: var(--font-main);
                font-size: 28px;
                font-style: normal;
                font-weight: 700;
                line-height: normal;
            }
        }
    }
    .conclusion {
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 16px;
        width: 100%;
        h4 {
            color: rgba(29, 29, 29, 0.5);
            font-family: var(--font-main);
            font-size: 14px;
            font-style: normal;
            font-weight: 800;
            line-height: normal;
        }
        p {
            color: var(--Text, #1d1d1d);
            text-align: center;
            font-family: var(--font-main);
            font-size: 20px;
            font-style: normal;
            font-weight: 500;
            line-height: 130%; /* 26px */
        }
    }
    .btns {
        display: flex;
        flex-direction: column;
        gap: 16px;
        width: 100%;
    }
    .recomendations {
        display: flex;
        flex-direction: column;
        gap: 16px;
        width: 100%;
        padding-bottom: 72px;
        h4 {
            color: var(--Text, #1d1d1d);
            font-size: 20px;
            font-style: normal;
            font-weight: 700;
            line-height: 130%; /* 26px */
        }
        p {
            color: rgba(29, 29, 29, 0.7);

            font-size: 16px;
            font-style: normal;
            font-weight: 400;
            line-height: 130%; /* 20.8px */
        }
    }
}
.skeleton {
    background-color: #e0e0e0; // Цвет фона для скелетонов
    border-radius: 4px;
    animation: shimmer 1.5s infinite linear;
}

.circlePhotoSkeleton {
    width: 152px;
    height: 152px;
    border-radius: 50%;
}

.resultTextSkeleton {
    height: 28px; // Высота для текстового скелетона
    width: 100px; // Ширина, которая будет изменяться в зависимости от текста
    margin: 4px 0; // Отступы
}

.conclusionSkeleton {
    height: 20px; // Высота для текстового скелетона
    width: 100%; // Ширина на всю ширину
    margin: 4px 0; // Отступы
}

.recommendationsSkeleton {
    height: 16px; // Высота для текстового скелетона
    width: 100%; // Ширина на всю ширину
    margin: 4px 0; // Отступы
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
    display: flex;
    flex-direction: column;
    gap: 16px;
    .txt {
        font-size: 16px;
        color: #1d1d1d;
    }
    .close-btn {
        width: 100%;
        display: flex;
        height: 48px;
        padding: 0px 24px;
        justify-content: center;
        align-items: center;
        gap: 8px;
        align-self: stretch;
        border-radius: 12px;
        background: #418af9;
        color: var(--Main, #fafafa);
        text-align: center;
        font-family: var(--font-main);
        font-size: 16px;
        font-style: normal;
        font-weight: 600;
        line-height: 24px; /* 150% */
    }
}
@keyframes shimmer {
    0% {
        background-position: -100px 0;
    }
    100% {
        background-position: 100px 0;
    }
}
</style>
