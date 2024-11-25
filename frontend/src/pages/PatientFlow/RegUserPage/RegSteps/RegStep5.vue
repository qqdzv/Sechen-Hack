<template>
    <div class="step5">
        <h2>Сколько тебе лет?</h2>
        <CustomInput v-model="ageValue" label-txt="Возраст" typeInp="text" />
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
    name: 'RegStep5',
});
const props = defineProps<{ age?: string }>();
const emit = defineEmits(['next-step', 'update:age', 'prev-step']);

const ageValue = ref(props.age || '');

watch(ageValue, (newAge) => {
    emit('update:age', newAge);
});

const nextStep = () => {
    if (ageValue.value) {
        emit('next-step');
    }
};
const prevStep = () => {
    emit('prev-step');
};
</script>
<style lang="scss" scoped>
.step5 {
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
