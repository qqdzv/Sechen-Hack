<template>
    <div class="step3">
        <h2>
            Придумай пароль,<br />
            пожалуйста
        </h2>
        <CustomInput v-model="passwordValue" label-txt="Password" typeInp="password" />
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
    name: 'RegStep3',
});
const props = defineProps<{ password?: string }>();
const emit = defineEmits(['next-step', 'update:password', 'prev-step']);

const passwordValue = ref(props.password || '');

watch(passwordValue, (newPassword) => {
    emit('update:password', newPassword);
});

const nextStep = () => {
    if (passwordValue.value) {
        emit('next-step');
    }
};
const prevStep = () => {
    emit('prev-step');
};
</script>
<style lang="scss" scoped>
.step3 {
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
