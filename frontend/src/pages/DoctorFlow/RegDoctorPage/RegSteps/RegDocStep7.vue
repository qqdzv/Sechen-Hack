<template>
    <div class="step7">
        <h2>Какой вуз Вы закончили?</h2>
        <CustomInput v-model="universityValue" label-txt="Университет" typeInp="text" />
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
    name: 'RegDocStep7',
});
const props = defineProps<{ university?: string }>();
const emit = defineEmits(['next-step', 'update:university', 'prev-step']);

const universityValue = ref(props.university || '');

watch(universityValue, (newUniversity) => {
    emit('update:university', newUniversity);
});

const nextStep = () => {
    if (universityValue.value) {
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
    gap: 88px;
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
