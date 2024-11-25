<template>
    <main class="folder">
        <h3>{{ isLoading ? 'Загрузка...' : folder?.folder_name }}</h3>
        <div class="scans">
            <div v-for="n in 3" :key="n" class="skeleton-scan" v-if="isLoading">
                <div class="skeleton skeleton-img"></div>
                <div class="skeleton-text">
                    <div class="skeleton skeleton-text-line"></div>
                    <div class="skeleton skeleton-text-line small"></div>
                </div>
            </div>
            <div v-else v-for="scan in folder?.scans" :key="scan.id" class="scan" @click="router.push({path:'/scanReport', query:{scanID: scan.id}})">
                <img :src="scan.image_base64" alt="scan" />
                <div class="texts">
                    <h4>{{ extractTextInParentheses(scan.response) || scan.response}}</h4>
                    <div class="date"><CustomIcon id="clock" :width="24" :height="24" /> {{ formatDate(scan.created_at).date }}</div>
                </div>
                <CustomIcon id="blueArrow" :width="24" :height="24" class="blueArrow" />
            </div>
        </div>
    </main>
</template>

<script setup lang="ts">
import api from '@/axios/api';
import { useScansStore } from '@/store/useScansStore';
import { useUserStore } from '@/store/useUserStore';
import CustomIcon from '@/ui/CustomIcon.vue';
import { formatDate } from '@/utils/fortmatDate';
import { extractTextInParentheses } from '@/utils/getTxtByRegxp';

import { computed, onMounted, ref } from 'vue';
import { useRoute, useRouter } from 'vue-router';

defineOptions({
    name: 'FolderPage',
});

interface Scan {
    id:number;
    folder_id:number;
    response:string;
    percent:number;
    type:string;
    result:string;
    recommendations:string;
    image_base64:string;
    created_at:string;
}

const route = useRoute();
const folderID = Number(route.params.id);
const folders = useScansStore().folders;
const userStore = useUserStore();
const isLoading = ref(true);
const router = useRouter(); 
const folder = computed(() => {
    return folders?.find((folder) => folder.id === folderID) || null;
});
const fetchScansForFolder = async (folderId: number) => {
    const scansStore = useScansStore();
    const folders = scansStore.getFolders();

    if (folders && folders.length > 0) {
        const response = await api.getData<Scan[]>(`/scan/history/${folderId}`);
        const folder = folders.find((folder) => folder.id === folderId);
        if (folder) {
            folder.scans = response;
            console.log(folder.scans);
            
            // Обновляем массив сканов в фолдере
        }

        isLoading.value = false;
    } else {
        console.error('No folders available in the store');
    }
};
onMounted(() => {
    fetchScansForFolder(folderID);
});
</script>

<style lang="scss" scoped>
.folder {
    width: 100%;
    height: 100%;

    h3 {
        color: var(--Text, #1d1d1d);
        font-family: var(--font-main);
        font-size: 24px;
        font-style: normal;
        font-weight: 800;
        line-height: normal;
    }

    .scans {
        margin-top: 28px;
        display: flex;
        flex-direction: column;
        gap: 12px;
        width: 100%;
        height: auto;
        overflow-y: scroll;
        padding-bottom: 72px;

        .scan,
        .skeleton-scan {
            position: relative;
            display: flex;
            width: 100%;
            height: 96px;
            border-bottom: 1px solid rgba(217, 217, 217, 0.5);
            align-items: start;
            flex-direction: row;
            gap: 16px;
        }

        .scan {
            h4 {
                color: #000;
                font-family: var(--font-main);
                font-size: 20px;
                font-style: normal;
                font-weight: 700;
                line-height: normal;
            }

            .date {
                display: flex;
                height: 24px;
                gap: 8px;
                align-items: center;
                color: rgba(29, 29, 29, 0.5);
                font-family: var(--font-main);
                font-size: 14px;
                font-style: normal;
                font-weight: 600;
                line-height: normal;
            }

            img {
                width: 75px;
                height: 75px;
                border-radius: 12px;
            }

            .blueArrow {
                position: absolute;
                right: 5px;
                bottom: 50%;
                transform: translateX(-50%);
            }
        }

        .skeleton {
            background: #e0e0e0;
            border-radius: 4px;
            animation: pulse 1.5s infinite ease-in-out;
        }

        .skeleton-img {
            width: 75px;
            height: 75px;
            border-radius: 12px;
        }

        .skeleton-text {
            display: flex;
            flex-direction: column;
            gap: 8px;
            width: 70%;

            .skeleton-text-line {
                height: 16px;
                width: 70%;
            }

            .skeleton-text-line.small {
                width: 40%;
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
