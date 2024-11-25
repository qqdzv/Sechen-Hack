<template>
    <div class="step4">
        <h2>Когда появились жалобы на кожу?</h2>
        <div class="groupBtns">
            <MainButton text="< 1 дня" @click="selectAnswer('< 1 дня')" :key="task4Value === '< 1 дня' ? 'male-button' : 'base-male'" :type="task4Value === '< 1 дня' ? 'primary' : 'base'" :style="{ width: '100%' }" />
            <MainButton text="1 - 7 дней " @click="selectAnswer('1 - 7 дней ')" :key="task4Value === '1 - 7 дней ' ? 'male-button' : 'base-male'" :type="task4Value === '1 - 7 дней ' ? 'primary' : 'base'" :style="{ width: '100%' }" />
            <MainButton text="1 - 4 недели" @click="selectAnswer('1 - 4 недели')" :key="task4Value === '1 - 4 недели' ? 'male-button' : 'base-male'" :type="task4Value === '1 - 4 недели' ? 'primary' : 'base'" :style="{ width: '100%' }" />
            <MainButton text="1 - 3 месяца" @click="selectAnswer('1 - 3 месяца')" :key="task4Value === '1 - 3 месяца' ? 'male-button' : 'base-male'" :type="task4Value === '1 - 3 месяца' ? 'primary' : 'base'" :style="{ width: '100%' }" />
            <MainButton text="Более 3 месяцев" @click="selectAnswer('Более 3 месяцев')" :key="task4Value === 'Более 3 месяцев' ? 'male-button' : 'base-male'" :type="task4Value === 'Более 3 месяцев' ? 'primary' : 'base'" :style="{ width: '100%' }" />
            <MainButton text="С рождения" @click="selectAnswer('С рождения')" :key="task4Value === 'С рождения' ? 'male-button' : 'base-male'" :type="task4Value === 'С рождения' ? 'primary' : 'base'" :style="{ width: '100%' }" />
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
    name: 'TestStep4',
});

const props = defineProps<{ task4?: string }>();
const emit = defineEmits(['next-step', 'update:task4', 'prev-step']);
const task4Value = ref(props.task4 || '');

watch(task4Value, (newAnswer) => {
    emit('update:task4', newAnswer);
});

const selectAnswer = (task: string) => {
    task4Value.value = task;
};

const nextStep = () => {
    if (task4Value.value) {
        emit('next-step');
    }
};

const prevStep = () => {
    emit('prev-step');
};
</script>

<style lang="scss" scoped>
.step4 {
    display: flex;
    flex-direction: column;
    gap: 8px;
    width: 100%;
    height: 100%;
    .groupBtns {
        display: flex;
        flex-direction: column;
        width: 100%;
        justify-content: space-between;
        gap: 8px;
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
    bottom: 30px;
    display: flex;
    flex-direction: row;
    justify-content: space-between;
}
</style>
