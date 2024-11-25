<template>
    <LoaderComp v-if="isLoading" />
    <router-view v-else />
</template>
<script setup lang="ts">
import './styles/global.scss';
import './styles/variables.scss';
import { ref, onMounted } from 'vue';
import LoaderComp from './components/LoaderComp.vue';
import { useRouter } from 'vue-router';

const isLoading = ref(true);
const router = useRouter();
onMounted(() => {
    setTimeout(() => {
        isLoading.value = false;
        router.push('/select');
    }, 5100); // Условное время загрузки
});
</script>
