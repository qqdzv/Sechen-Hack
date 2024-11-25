<template>
    <div class="loading-screen">
        <svg class="progress-circle" viewBox="0 0 36 36">
            <path class="circle-background" d="M18 2a16 16 0 1 1 0 32 16 16 0 1 1 0-32" />
            <path class="circle-progress" :stroke-dasharray="`${progress}, 100`" d="M18 2a16 16 0 1 1 0 32 16 16 0 1 1 0-32" />
        </svg>
        <div class="loading-text">{{ progress }}%</div>
    </div>
</template>

<script lang="ts" setup>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
const emit = defineEmits(['load-analys']);
// Создаем переменную, чтобы отслеживать процент загрузки
const progress = ref<number>(0);
const router = useRouter();
onMounted(() => {
    // Интервал для имитации загрузки
    const loadingInterval = setInterval(() => {
        if (progress.value < 100) {
            progress.value += 1; // Увеличиваем значение на 1% каждую сотую секунду
        } else {
            emit('load-analys');
            clearInterval(loadingInterval); // Останавливаем интервал, когда загрузка завершена
        }
    }, 110);
});
</script>

<style scoped>
.loading-screen {
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    height: 100vh;
    position: relative;
}

.progress-circle {
    width: 150px;
    height: 150px;
    rotate: 90deg;
}

.circle-background {
    fill: #3b74d5;
    stroke-width: 2;
}

.circle-progress {
    fill: none;
    stroke: #fff;
    stroke-width: 2;
    stroke-linecap: round;
    transform: rotate(-90deg);
    transform-origin: 50% 50%;
    transition: stroke-dasharray 0.3s ease;
}

.loading-text {
    position: absolute;
    bottom: 50%;
    transform: translateY(50%);
    color: #fff;
    font-family: var(--font-main);
    font-size: 40px;
    font-style: normal;
    font-weight: 800;
    line-height: 24px; /* 60% */
}
</style>
