<template>
    <div class="step2">
        <h2>У Вас есть домашние животные с шерстью?</h2>
        <div class="groupBtns">
            <MainButton text="Нет" :key="task2Value === 'Нет' ? 'male-button' : 'base-male'" @click="selectAnswer('Нет')" :type="task2Value === 'Нет' ? 'primary' : 'base'" :width="165" />
            <MainButton text="Да" @click="selectAnswer('Да')" :key="task2Value === 'Да' ? 'male-button' : 'base-male'" :type="task2Value === 'Да' ? 'primary' : 'base'" :width="165" />
        </div>
    </div>
    <div class="bottom">
        <MainButton text="Назад" @click="prevStep" type="secondary" />
        <MainButton text="Далее" @click="nextStep" type="primary" />
    </div>
</template>

<script setup lang="ts">
import { defineProps, defineEmits, ref, watch } from 'vue';
import MainButton from '@/ui/MainButton.vue';

defineOptions({
    name: 'TestStep2',
});

const props = defineProps<{ task2?: string }>();
const emit = defineEmits(['next-step', 'update:task2', 'prev-step']);
const task2Value = ref(props.task2 || '');

watch(task2Value, (newAnswer) => {
    emit('update:task2', newAnswer);
});

const selectAnswer = (task: string) => {
    task2Value.value = task;
};

const nextStep = () => {
    if (task2Value.value) {
        emit('next-step');
    }
};

const prevStep = () => {
    emit('prev-step');
};
</script>

<style lang="scss" scoped>
.step2 {
    display: flex;
    flex-direction: column;
    gap: 68px;
    width: 100%;
    height: 100%;
    .groupBtns {
        display: flex;
        flex-direction: row;
        width: 100%;
        justify-content: space-between;
    }
    h2 {
        color: var(--Text, #1d1d1d);
        font-family: var(--font-main);
        font-size: 32px;
        font-style: normal;
        font-weight: 600;
        line-height: normal;
    }
}
.bottom {
    position: fixed;
    width: 89.7435897vw;
    bottom: 50px;
    display: flex;
    flex-direction: row;
    justify-content: space-between;
}
</style>
