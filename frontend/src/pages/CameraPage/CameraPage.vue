<template>
    <main class="testLayout" v-if="!photoSelected">
        <CustomIcon id="logo" :width="207" :height="33" className="logo" />
        <div class="testPage" v-if="isPatient">
            <TestStep1 v-if="step === 1" v-model:task1="formData.folder_name" @prev-step="handlePrevStep" @next-step="handleNextStep" @skip-test="handleSkipTest" />
            <TestStep2 v-if="step === 2" v-model:task2="formData.body_part" @next-step="handleNextStep" @prev-step="handlePrevStep" />
            <TestStep3 v-if="step === 3" v-model:task3="formData.size" @next-step="handleNextStep" @prev-step="handlePrevStep" />
            <TestStep4 v-if="step === 4" v-model:task4="formData.how_many_days" @next-step="handleNextStep" @prev-step="handlePrevStep" />
            <TestStep5 v-if="step === 5" v-model:task5="formData.have_pain" @next-step="handleNextStep" @prev-step="handlePrevStep" />
            <TestStep6 v-if="step === 6" v-model:task6="formData.have_medicines" @next-step="handleNextStep" @prev-step="handlePrevStep" />
            <TestStep7 v-if="step === 7 || step === 8" v-model:task7="formData.mixing" @next-step="handleNextStep" @prev-step="handlePrevStep" />
        </div>
        <div class="testPage" v-else>
            <TestStep2 v-if="step === 1" v-model:task2="formData.body_part" @next-step="handleNextStep" @prev-step="handlePrevStep"/>
            <TestDocStep2 v-if="step === 2" v-model:gender="formData.gender" @next-step="handleNextStep" @prev-step="handlePrevStep" />
            <TestDocStep3 v-if="step === 3 || step === 4" v-model:age="formData.age" @next-step="handleNextStep" @prev-step="handlePrevStep" />
        </div>
        <div class="modal_overlay" v-if="openModal" @click="closeModal"></div>
        <div class="modal" v-if="openModal">
            <div class="file-btn">
                <input type="file" id="file" class="file-input" @change="onFileChange" />
                <label for="file" class="file-label">Выберите файл</label>
            </div>
            <button @click="closeModal" class="close-btn">Закрыть</button>
        </div>
    </main>
    <TakePhoto v-if="photoSelected" v-model:task8="formData.image_base64" @submit="handleTestSubmit" v-model:imageUrl="imageUrl" />

    <p v-if="errorTxt" style="color: red">{{ errorTxt }}</p>
</template>

<script setup lang="ts">
import { computed, ref } from 'vue';

import TakePhoto from './CameraTest/TakePhoto.vue';
import TestStep1 from './CameraTest/TestStep1.vue';
import TestStep2 from './CameraTest/TestStep2.vue';
import TestStep3 from './CameraTest/TestStep3.vue';
import TestStep4 from './CameraTest/TestStep4.vue';
import TestStep5 from './CameraTest/TestStep5.vue';
import TestStep6 from './CameraTest/TestStep6.vue';
import TestStep7 from './CameraTest/TestStep7.vue';
import CustomIcon from '@/ui/CustomIcon.vue';
import { useUserStore } from '@/store/useUserStore';
import { useRouter } from 'vue-router';
import TestDocStep2 from './CameraTest/TestDocStep2.vue';
import TestDocStep3 from './CameraTest/TestDocStep3.vue';
import { Scan } from '@/store/useScansStore';

const step = ref<number>(1);
const userStore = useUserStore();
const isPatient = computed(() => (userStore.user?.role === 'user' ? true : false));
const postResponse = ref<Scan | null>(null);
const errorTxt = ref<string | null>(null);
const photoSelected = computed(() => imageUrl.value !== '');
const openModal = ref<boolean>(false);
const imageUrl = ref<string>('');
const router = useRouter();
const formData = ref<PostData>({
    body_part: '',
    image_base64: '',
    gender: '',
    age: '',
});

function handleNextStep() {
    if (step.value < 8) {
        if (step.value < 8) {
            if (isPatient.value) {
                step.value++;
            } else {
                // Если не пациент и на 4 шаге, открыть модальное окно
                if (step.value === 4) {
                    openModal.value = true;
                } else {
                    step.value++;
                }
            }
        }
        if (step.value === 8) {
            openModal.value = true;
        }
        console.log(step.value);
    }
}
function handleSkipTest() {
    console.log(openModal.value);

    openModal.value = true;
}
function closeModal() {
    openModal.value = false;
}

const onFileChange = (event: Event) => {
    const target = event.target as HTMLInputElement;
    if (target.files && target.files.length > 0) {
        const file = target.files[0];
        const reader = new FileReader();

        reader.onload = (e) => {
            imageUrl.value = e.target?.result as string;
        };
        reader.readAsDataURL(file);

        console.log(imageUrl.value);
    }
};

interface PostData {
    folder_name?: string;
    body_part: string;
    size?: string;
    how_many_days?: string;
    have_pain?: boolean;
    have_medicines?: boolean;
    mixing?: string;
    image_base64: string;
    gender: string;
    age: string;
}

const handleTestSubmit = () => {
    router.push({ path: '/quiz', query: { formData: JSON.stringify(formData.value) } });
};

function handlePrevStep() {
    console.log(step.value);
    
    if (step.value > 1) {
        step.value--;
    }
    else{
        router.push('/select');
    }
}
</script>

<style lang="scss" scoped>
.testLayout {
    width: 100%;
    padding-top: 36px;
    display: flex;
    flex-direction: column;
    align-items: center;
    height: 100dvh;

    .logo {
        position: relative;
        width: 207px;
        height: 33px;
        z-index: 6;
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
        bottom: 0;
        left: 50%;
        transform: translateX(-50%);
        padding: 20px;
        z-index: 6;
        border-radius: 8px;
        width: 90%;
        font-family: var(--font-main);
        font-weight: 600;
        .file-btn {
            display: flex;
            align-items: center;
            width: 100%;
            justify-content: center;
            margin-bottom: 10px;
            .file-input {
                display: none; /* скрывает оригинальный input */
            }

            .file-label {
                color: var(--Main, #418af9);
                text-align: center;
                font-family: var(--font-main);
                font-size: 16px;
                font-style: normal;
                font-weight: 600;
                line-height: 24px; /* 150% */
                width: 100%;
                text-align: center;
                padding: 10px 20px;
                background-color: #fff;
                border-radius: 12px;
                cursor: pointer;
                transition: background-color 0.3s;
            }

            .file-label:hover {
                background-color: #0056b3;
            }

            .file-name {
                margin-left: 15px;
                font-size: 0.9rem;
                color: #333;
            }
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
            background: #fff;
            color: var(--Main, #418af9);
            text-align: center;
            font-family: var(--font-main);
            font-size: 16px;
            font-style: normal;
            font-weight: 600;
            line-height: 24px; /* 150% */
        }
    }
}

.testPage {
    margin-top: 20px;
    width: 100%;
    padding: 0 20px;
}
</style>
