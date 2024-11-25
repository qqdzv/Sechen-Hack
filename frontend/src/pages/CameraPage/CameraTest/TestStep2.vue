<template>
    <div class="step2">
        <h2>Какую часть тела вы хотите сканировать?</h2>
        <CustomDropDown v-model="task2Value" :options="options" placeholder="Выберите часть тела" text="Часть тела" />
    </div>
    <div class="bottom">
        <MainButton text="Назад" @click="prevStep" type="secondary" />
        <MainButton text="Далее" @click="nextStep" type="primary" :disabled="!task2Value" />
    </div>
</template>

<script setup lang="ts">
import { defineProps, defineEmits, ref, watch } from 'vue';
import MainButton from '@/ui/MainButton.vue';
import CustomDropDown from '@/ui/CustomDropDown.vue';
import { translateToLat } from '@/utils/getRusText';

defineOptions({
    name: 'TestStep2',
});
const options = ['Передняя часть торса', 'Нижняя конечность', 'Голова/шея', 'Верхняя конечность', 'Задняя часть торса', 'Ладони/подошвы', 'Полость рта/гениталии', 'Боковая часть торса'];
const props = defineProps<{ task2?: string | null }>();
const emit = defineEmits(['next-step', 'update:task2', 'prev-step']);
const task2Value = ref(props.task2 || '');
watch(task2Value, (newAnswer) => {
    emit('update:task2', newAnswer);
});

const nextStep = () => {
    if (task2Value.value) {
        emit('update:task2', translateToLat(task2Value.value));
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
    gap: 38px;
    width: 100%;
    height: 100%;
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
