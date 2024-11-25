<template>
    <div class="quizHeader">
        <div class="progress_text">
            <p>Анализ данных...</p>
            <p>{{ percentage }}%</p>
        </div>
        <div class="progress_bar" v-if="percentage < 100">
            <div class="progress" :style="{ width: percentage + '%' }"></div>
        </div>
        <MainButton v-if="percentage === 100" text="Перейти к анализу" type="base" style="width: 100%" @click="emit('load-analys')" />
    </div>
</template>
<script setup lang="ts">
import MainButton from '@/ui/MainButton.vue';
import { onMounted, ref } from 'vue';
const emit = defineEmits(['load-analys']);
const percentage = ref<number>(0);
onMounted(() => {
    const loadingInterval = setInterval(() => {
        if (percentage.value < 100) {
            percentage.value += 1; // Увеличиваем значение на 1% каждую сотую секунду
        } else {
            clearInterval(loadingInterval); // Останавливаем интервал, когда загрузка завершена
        }
    }, 200);
});
</script>
<style lang="scss" scoped>
.quizHeader {
    margin-top: 10px;
    width: 100%;
    display: flex;
    flex-direction: column;
    gap: 8px;
    height: auto;
    .progress_text {
        display: flex;
        flex-direction: row;
        justify-content: space-between;

        color: var(--bg-1, #fafafa);
        font-family: var(--font-main);
        color: #fff;
        font-family: var(--font-main);
        font-size: 14px;
        font-style: normal;
        font-weight: 900;
        line-height: normal;
    }
    .progress_bar {
        width: 100%;
        height: 5px;
        border-radius: 30px;
        background: rgba(250, 250, 250, 0.3);
        .progress {
            border-radius: 30px;
            height: 5px;
            background: #fafafa;
        }
    }
}
</style>
