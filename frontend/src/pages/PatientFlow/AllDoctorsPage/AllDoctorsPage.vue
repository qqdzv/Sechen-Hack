<template>
    <main class="doctorsPage">
        <h3>{{ isLoading ? 'Загрузка...' : 'Консультация с врачом' }}</h3>
        <div class="doctors">
            <div v-if="isLoading" class="doctor skeleton-doctor" v-for="n in 3" :key="n">
                <div class="profile">
                    <div class="initials skeleton skeleton-text"></div>
                    <div class="doc_info">
                        <h4 class="flname skeleton skeleton-text"></h4>
                        <div class="text skeleton skeleton-text"></div>
                    </div>
                </div>
                <h4 class="university skeleton skeleton-text"></h4>
                <div class="skeleton skeleton-button"></div>
            </div>
            <div v-else v-for="doctor in doctors" :key="doctor.id" class="doctor" @click="">
                <div class="profile">
                    <div class="initials">
                        <p class="bukv">{{ doctor.first_name[0].toUpperCase() + doctor.last_name[0].toUpperCase() }}</p>
                    </div>
                    <div class="doc_info">
                        <h4 class="flname">{{ doctor.first_name }} {{ doctor.last_name }}</h4>
                        <div class="text">
                            <CustomIcon id="verify" :width="24" :height="24" />
                            {{ doctor.experience_age + ' лет ' }}
                             •
                            <CustomIcon id="doctor" :width="24" :height="24" />
                            {{ doctor.speciality }}
                        </div>
                    </div>
                </div>
                <h4 class="university">{{ doctor.university }}</h4>
                <MainButton text="Написать" type="secondary" style="width: 100%" @click="router.push(`/chat/${doctor.id}`)"/>
            </div>
        </div>
    </main>
    <MenuComp />
</template>

<script setup lang="ts">
import api from '@/axios/api';
import MenuComp from '@/components/MenuComp.vue';
import { useScansStore } from '@/store/useScansStore';
import { Doctor, useUserStore } from '@/store/useUserStore';
import CustomIcon from '@/ui/CustomIcon.vue';
import MainButton from '@/ui/MainButton.vue';
import { formatDate } from '@/utils/fortmatDate';

import { computed, onMounted, ref } from 'vue';
import { useRoute, useRouter } from 'vue-router';

defineOptions({
    name: 'FolderPage',
});

interface Scan {
    id: number;
    folder_id: number;
    response: string;
    percent: number;
    type: string;
    result: string;
    recommendations: string;
    image_base64: string;
    created_at: string;
}

const route = useRoute();
const folderID = Number(route.params.id);
const folders = useScansStore().folders;
const userStore = useUserStore();
const isLoading = ref(true);
const router = useRouter();
const doctors = ref<Doctor[]>([]);
const fetchAllDoctors = async () => {
    try {
        const response = await api.getData<Doctor[]>(`/doctor/get_all_doctors`);
        return response;
    } catch (error) {
        console.error('Error fetching doctors:', error);
    } finally {
        isLoading.value = false;
    }
};
onMounted(async () => {
    const fetchedDoctors = await fetchAllDoctors();
    if (fetchedDoctors) {
        doctors.value = fetchedDoctors;
        console.log(fetchedDoctors);
        
    }
});
</script>

<style lang="scss" scoped>
.doctorsPage {
    width: 100%;
    height: 100%;
    font-family: var(--font-main);
    padding: 10px 20px 72px 20px;
    h3 {
        color: var(--Text, #1d1d1d);
        font-size: 24px;
        font-weight: 800;
    }

    .doctors {
        margin-top: 28px;
        display: flex;
        flex-direction: column;
        gap: 20px;
        width: 100%;
        overflow-y: scroll;
        padding-bottom: 78px;

        .doctor {
            display: flex;
            flex-direction: column;
            gap: 16px;
            padding: 16px;
            border-radius: 24px;
            background: #fff;
            box-shadow: 8px 8px 104px 0px rgba(0, 0, 0, 0.04);

            .profile {
                display: flex;
                gap: 12px;

                .initials {
                    width: 65px;
                    height: 65px;
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    background-color: #f7f7f7;
                    border-radius: 12px;
                    .bukv {
                        font-size: 24px;
                        font-weight: 700;
                        color: #020202;
                        opacity: 0.1;
                    }
                }
                
                .doc_info {
                    display: flex;
                    flex-direction: column;
                    gap: 4px;
                    .flname {
                        color: var(--Text, #1d1d1d);
                        font-size: 18px;
                        font-weight: 800;
                    }
                    .text {
                        display: flex;
                        gap: 8px;
                        color: #8d93a5;
                        font-size: 14px;
                        font-weight: 500;
                    }
                }
            }

            .university {
                color: var(--Text, #1d1d1d);
                font-size: 18px;
                font-weight: 700;
            }
        }

        /* Skeleton styles */
        .skeleton-doctor {
            .initials, .flname, .text, .university, .skeleton-button {
                background: #e0e0e0;
                animation: pulse 1.5s ease-in-out infinite;
                border-radius: 4px;
            }
            .initials {
                height: 65px;
                width: 65px;
            }
            .flname {
                height: 18px;
                width: 100px;
                margin-bottom: 8px;
            }
            .text {
                height: 14px;
                width: 150px;
                margin-bottom: 8px;
            }
            .university {
                height: 18px;
                width: 120px;
            }
            .skeleton-button {
                height: 40px;
                width: 100%;
                margin-top: 16px;
                border-radius: 8px;
            }
        }
    }
}

@keyframes pulse {
    0% {
        opacity: 1;
    }
    50% {
        opacity: 0.4;
    }
    100% {
        opacity: 1;
    }
}
</style>