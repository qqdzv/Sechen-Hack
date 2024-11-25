<template>
    <div class="step7">
        <h2>
            Замечали ли вы <br />
            в родинке смешивание нескольких цветов (коричневый, черный, красный и т.д.)?
        </h2>
        <div class="groupBtns">
            <MainButton text="Да, несколько цветов" @click="selectAnswer('Да, несколько цветов')" :key="task7Value === 'Да, несколько цветов' ? 'male-button' : 'base-male'" :type="task7Value === 'Да, несколько цветов' ? 'primary' : 'base'" :style="{ width: '100%' }" />
            <MainButton text="Нет, один цвет" @click="selectAnswer('Нет, один цвет')" :key="task7Value === 'Нет, один цвет' ? 'male-button' : 'base-male'" :type="task7Value === 'Нет, один цвет' ? 'primary' : 'base'" :style="{ width: '100%' }" />
            <MainButton text="Не уверен(а)" @click="selectAnswer('Не уверен(а)')" :key="task7Value === 'Не уверен(а)' ? 'male-button' : 'base-male'" :type="task7Value === 'Не уверен(а)' ? 'primary' : 'base'" :style="{ width: '100%' }" />
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
    name: 'TestStep7',
});

const props = defineProps<{ task7?: string }>();
const emit = defineEmits(['next-step', 'update:task7', 'prev-step']);
const task7Value = ref(props.task7 || '');

watch(task7Value, (newAnswer) => {
    emit('update:task7', newAnswer);
});

const selectAnswer = (task: string) => {
    task7Value.value = task;
};

const nextStep = () => {
    if (task7Value.value) {
        emit('next-step');
    }
};

const prevStep = () => {
    emit('prev-step');
};
</script>

<style lang="scss" scoped>
.step7 {
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
