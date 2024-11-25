<template>
    <div class="step1">
        <h2>Вы уже лечили изменения на коже?</h2>
        <div class="groupBtns">
            <MainButton text="Нет" :key="task1Value === 'Нет' ? 'male-button' : 'base-male'" @click="selectAnswer('Нет')" :type="task1Value === 'Нет' ? 'primary' : 'base'" :width="165" />
            <MainButton text="Да" @click="selectAnswer('Да')" :key="task1Value === 'Да' ? 'male-button' : 'base-male'" :type="task1Value === 'Да' ? 'primary' : 'base'" :width="165" />
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
import { useRouter } from 'vue-router';

defineOptions({
    name: 'TestStep1',
});

const props = defineProps<{ task1?: string }>();
const emit = defineEmits(['next-step', 'update:task1', 'prev-step']);
const task1Value = ref(props.task1 || '');

watch(task1Value, (newAnswer) => {
    emit('update:task1', newAnswer);
});

const selectAnswer = (task: string) => {
    task1Value.value = task;
};

const nextStep = () => {
    if (task1Value.value) {
        emit('next-step');
    }
};

const prevStep = () => {
    window.history.back();
};
</script>

<style lang="scss" scoped>
.step1 {
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
