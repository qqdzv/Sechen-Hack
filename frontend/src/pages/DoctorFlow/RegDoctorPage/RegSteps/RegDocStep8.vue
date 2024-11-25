<template>
    <div class="step8">
        <h2>Какая у Вас специализация?</h2>
        <CustomInput v-model="specialityValue" label-txt="Специализация" typeInp="text" />
    </div>
    <div class="bottom">
        <MainButton text="Назад" @click="prevStep" type="secondary" />
        <MainButton text="Далее" @click="submit" type="primary" />
    </div>
</template>
<script setup lang="ts">
import { defineProps, defineEmits, ref, watch } from 'vue';
import CustomInput from '@/ui/CustomInput.vue';
import MainButton from '@/ui/MainButton.vue';

defineOptions({
    name: 'RegDocStep8',
});
const props = defineProps<{ speciality?: string }>();
const emit = defineEmits(['submit', 'update:speciality', 'prev-step']);

const specialityValue = ref(props.speciality || '');

watch(specialityValue, (newSpeciality) => {
    emit('update:speciality', newSpeciality);
});

const submit = () => {
    if (specialityValue.value) {
        emit('submit');
    }
};
const prevStep = () => {
    emit('prev-step');
};
</script>
<style lang="scss" scoped>
.step8 {
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
