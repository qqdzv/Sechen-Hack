<template>
    <div class="step2">
        <h2>
            Какую почту <br />
            ты хочешь привязать?
        </h2>
        <CustomInput v-model="emailValue" label-txt="Email" typeInp="email" />
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
    name: 'RegStep2',
});
const props = defineProps<{ email?: string }>();
const emit = defineEmits(['next-step', 'update:email', 'prev-step']);

const emailValue = ref(props.email || '');

watch(emailValue, (newEmail) => {
    emit('update:email', newEmail);
});

const nextStep = () => {
    const emailRegex = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
    if (emailRegex.test(emailValue.value)) {
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
