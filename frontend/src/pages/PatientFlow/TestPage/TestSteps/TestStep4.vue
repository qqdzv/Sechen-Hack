<template>
    <div class="step4">
        <h2>Какая у Вас профессия?</h2>
        <CustomInput v-model="task4Value" label-txt="Профессия" typeInp="text" />
    </div>
    <div class="bottom">
        <MainButton text="Назад" @click="prevStep" type="secondary" />
        <MainButton text="Далее" @click="nextStep" type="primary" />
    </div>
</template>
<script setup lang="ts">
import { defineProps, defineEmits, ref, watch } from 'vue';
import CustomInput from '@/ui/CustomInput.vue';
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
    gap: 68px;
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
