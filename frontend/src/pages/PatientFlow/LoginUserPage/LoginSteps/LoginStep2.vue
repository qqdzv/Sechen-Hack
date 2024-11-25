<template>
    <div class="step2">
        <h2>
            Помнишь<br />
            свой пароль?
        </h2>
        <CustomInput v-model="passwordValue" label-txt="Password" typeInp="password" />
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

const props = defineProps<{ password: string }>();
const passwordValue = ref(props.password || '');
const emit = defineEmits(['update:password', 'prev-step', 'submit']);

watch(passwordValue, (newPassword) => {
    emit('update:password', newPassword); // Эмитируем новое значение
});

const submit = () => {
    emit('submit');
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
    h2 {
        color: var(--text-color, #1d1d1d);
        font-family: var(--font-main);
        font-size: 32px;
        font-style: normal;
        font-weight: 600;
        line-height: normal;
    }
}
.bottom {
    position: fixed;
    width: 89.744vw;
    bottom: 50px;
    display: flex;
    flex-direction: row;
    justify-content: space-between;
    margin-right: 20px;
}
</style>
