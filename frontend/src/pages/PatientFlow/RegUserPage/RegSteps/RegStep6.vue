<template>
    <div class="step6">
        <h2>
            Отлично!<br />
            Какой у тебя тип кожи?
        </h2>
        <div class="groupBtns">
            <SkinButton text="1" :key="skinTypeValue === '1' ? 'male-button' : 'base-male'" @click="selectSkinType('1')" :type="skinTypeValue === '1' ? 'primary' : 'base'" colorC="#F3E3CA" />
            <SkinButton text="2" :key="skinTypeValue === '2' ? 'male-button' : 'base-male'" @click="selectSkinType('2')" :type="skinTypeValue === '2' ? 'primary' : 'base'" colorC="#DFBC9E" />
            <SkinButton text="3" :key="skinTypeValue === '3' ? 'male-button' : 'base-male'" @click="selectSkinType('3')" :type="skinTypeValue === '3' ? 'primary' : 'base'" colorC="#E5BC8A" />
            <SkinButton text="4" :key="skinTypeValue === '4' ? 'male-button' : 'base-male'" @click="selectSkinType('4')" :type="skinTypeValue === '4' ? 'primary' : 'base'" colorC="#B4936A" />
            <SkinButton text="5" :key="skinTypeValue === '5' ? 'male-button' : 'base-male'" @click="selectSkinType('5')" :type="skinTypeValue === '5' ? 'primary' : 'base'" colorC="#855736" />
            <SkinButton text="6" :key="skinTypeValue === '6' ? 'male-button' : 'base-male'" @click="selectSkinType('6')" :type="skinTypeValue === '6' ? 'primary' : 'base'" colorC="#523E35" />
        </div>
    </div>
    <div class="bottom">
        <MainButton text="Назад" @click="prevStep" type="secondary" />
        <MainButton text="Далее" @click="submit" type="primary" />
    </div>
</template>

<script setup lang="ts">
import { defineProps, defineEmits, ref, watch } from 'vue';
import MainButton from '@/ui/MainButton.vue';
import SkinButton from './SkinButton.vue';

defineOptions({
    name: 'RegStep6',
});

const props = defineProps<{ skinType?: string }>();
const emit = defineEmits(['submit', 'update:skinType', 'prev-step']);

const skinTypeValue = ref(props.skinType || '');

watch(skinTypeValue, (newSkinType) => {
    emit('update:skinType', newSkinType);
});

const selectSkinType = (gender: string) => {
    skinTypeValue.value = gender;
};

const submit = () => {
    if (skinTypeValue.value) {
        emit('submit');
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
    gap: 32px;
    width: 100%;
    height: 100%;
    .groupBtns {
        display: grid;
        width: 100%;
        justify-content: space-between;
        grid-template-rows: 1fr 1fr;
        grid-template-columns: 1fr 1fr 1fr;
        gap: 7px;
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
