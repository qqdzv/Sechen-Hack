<template>
    <div class="step4">
        <h2>Каков твой гендер?</h2>
        <div class="groupBtns">
            <MainButton text="Мужской" :key="genderValue === 'male' ? 'male-button' : 'base-male'" @click="selectGender('male')" :type="genderValue === 'male' ? 'primary' : 'base'" :width="165" />
            <MainButton text="Женский" @click="selectGender('female')" :key="genderValue === 'male' ? 'male-button' : 'base-male'" :type="genderValue === 'female' ? 'primary' : 'base'" :width="165" />
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
    name: 'RegStep4',
});

const props = defineProps<{ gender?: string }>();
const emit = defineEmits(['next-step', 'update:gender', 'prev-step']);

const genderValue = ref(props.gender || '');

watch(genderValue, (newGender) => {
    emit('update:gender', newGender);
});

const selectGender = (gender: string) => {
    genderValue.value = gender;
};

const nextStep = () => {
    if (genderValue.value) {
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
