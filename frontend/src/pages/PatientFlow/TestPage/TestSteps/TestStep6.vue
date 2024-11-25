<template>
    <div class="step6">
        <h2>Часто ли вы загораете или посещаете солярий?</h2>
        <div class="groupBtns">
            <MainButton text="Часто, более 3 раз в месяц" @click="selectAnswer('Часто, более 3 раз в месяц')" :key="task6Value === 'Часто, более 3 раз в месяц' ? 'male-button' : 'base-male'" :type="task6Value === 'Часто, более 3 раз в месяц' ? 'primary' : 'base'" :style="{ width: '100%' }" />
            <MainButton text="Иногда, менее 3 раз в месяц" @click="selectAnswer('Иногда, менее 3 раз в месяц')" :key="task6Value === 'Иногда, менее 3 раз в месяц' ? 'male-button' : 'base-male'" :type="task6Value === 'Иногда, менее 3 раз в месяц' ? 'primary' : 'base'" :style="{ width: '100%' }" />
            <MainButton text="Никогда" @click="selectAnswer('Никогда')" :key="task6Value === 'Никогда' ? 'male-button' : 'base-male'" :type="task6Value === 'Никогда' ? 'primary' : 'base'" :style="{ width: '100%' }" />
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
    name: 'TestStep6',
});

const props = defineProps<{ task5?: string }>();
const emit = defineEmits(['next-step', 'update:task6', 'prev-step']);
const task6Value = ref(props.task5 || '');

watch(task6Value, (newAnswer) => {
    emit('update:task6', newAnswer);
});

const selectAnswer = (task: string) => {
    task6Value.value = task;
};

const nextStep = () => {
    if (task6Value.value) {
        emit('next-step');
    }
};

const prevStep = () => {
    emit('prev-step');
};
</script>

<style lang="scss" scoped>
.step6 {
    display: flex;
    flex-direction: column;
    gap: 18px;
    width: 100%;
    height: 100%;
    .groupBtns {
        display: flex;
        flex-direction: column;
        width: 100%;
        justify-content: space-between;
        row-gap: 10px;
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
