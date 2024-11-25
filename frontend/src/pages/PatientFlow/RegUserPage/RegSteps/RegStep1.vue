<template>
    <div class="step1">
        <h2>Как тебя зовут?</h2>
        <div class="inputsGroup">
            <CustomInput v-model="nameValue" label-txt="Твое имя" typeInp="text" />
            <CustomInput v-model="surnmameValue" label-txt="Твоя фамилия" typeInp="text" />
        </div>
    </div>
    <div class="bottom">
        <MainButton text="Войти" @click="router.push('/login/' + roleStore.role)" type="base" />
        <MainButton text="Далее" @click="nextStep" type="primary" />
    </div>
</template>
<script setup lang="ts">
import { defineProps, defineEmits, ref, watch } from 'vue';
import CustomInput from '@/ui/CustomInput.vue';
import MainButton from '@/ui/MainButton.vue';
import { useRouter } from 'vue-router';
import { useRoleStore } from '@/store/useRoleStore';

defineOptions({
    name: 'RegStep1',
});
const props = defineProps<{ name?: string; surname?: string }>();
const router = useRouter();
const emit = defineEmits(['next-step', 'update:surname', 'update:name']);
const roleStore = useRoleStore();
const nameValue = ref(props.name || '');
const surnmameValue = ref(props.surname || '');
watch(nameValue, (newName) => {
    emit('update:name', newName);
});
watch(surnmameValue, (newSurname) => {
    emit('update:surname', newSurname);
});
const nextStep = () => {
    if (nameValue.value && surnmameValue.value) {
        emit('next-step');
    }
};
</script>
<style lang="scss" scoped>
.step1 {
    display: flex;
    flex-direction: column;
    gap: 36px;
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
    .inputsGroup {
        display: flex;
        flex-direction: column;
        gap: 28px;
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
