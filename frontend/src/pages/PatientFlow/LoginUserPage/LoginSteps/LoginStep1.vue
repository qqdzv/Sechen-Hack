<template>
    <div class="step1">
        <h2>
            С возвращением!<br />
            Введи свой email
        </h2>
        <CustomInput v-model="emailValue" label-txt="Email" typeInp="text" />
    </div>
    <div class="bottom">
        <MainButton text="Регистрация" @click="router.push('/register/' + role.role)" />
        <MainButton text="Далее" @click="nextStep" type="primary" />
    </div>
</template>

<script setup lang="ts">
import { defineProps, defineEmits, ref, watch } from 'vue';
import CustomInput from '@/ui/CustomInput.vue';
import MainButton from '@/ui/MainButton.vue';
import { useRouter } from 'vue-router';
import { useRoleStore } from '@/store/useRoleStore';

const props = defineProps<{ email: string }>();
const emit = defineEmits(['update:email', 'next-step']);
const router = useRouter();
const emailValue = ref(props.email);
const role = useRoleStore();
watch(emailValue, (newEmail) => {
    emit('update:email', newEmail);
});

const nextStep = () => {
    emit('next-step');
};
</script>

<style lang="scss" scoped>
.step1 {
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
    width: 89.744vw;
    bottom: 50px;
    display: flex;
    flex-direction: row;
    justify-content: space-between;
    margin-right: 20px;
}
</style>
