<template>
    <div class="step1">
        <h2>
            Выберите папку <br />
            с Вашими старыми анализами или создайте новую
        </h2>
        <div class="groupBtns">
            <CustomDropDown v-model="task1Value" :options="options" placeholder="Выберите папку" text="Название существующем папки" />
            <span>или</span>
            <CustomInput v-model="task1Value" label-txt="Название новой папки" typeInp="text" />
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
import CustomDropDown from '@/ui/CustomDropDown.vue';
import { useUserStore } from '@/store/useUserStore';
import CustomInput from '@/ui/CustomInput.vue';
import { useScansStore } from '@/store/useScansStore';

defineOptions({
    name: 'TestStep1',
});

const props = defineProps<{ task1?: string }>();
const emit = defineEmits(['next-step', 'update:task1', 'prev-step', 'skip-test']);
const task1Value = ref(props.task1 || '');
const userStore = useUserStore();
const options =
    useScansStore()
        .getFolders()
        ?.map((folder) => folder.folder_name) || [];
watch(task1Value, (newAnswer) => {
    emit('update:task1', newAnswer);
});

const selectAnswer = (task: string) => {
    task1Value.value = task;
};

const nextStep = () => {
    if (task1Value.value) {
        if (options.includes(task1Value.value)) {
            emit('skip-test');
            console.log('fd');
        } else {
            emit('next-step');
        }
    }
};

const prevStep = () => {
    emit('prev-step');
};
</script>

<style lang="scss" scoped>
.step1 {
    display: flex;
    flex-direction: column;
    gap: 18px;
    width: 100%;
    height: 100%;
    .groupBtns {
        display: flex;
        flex-direction: column;
        width: 100%;
        justify-content: space-between;
        gap: 10px;
        align-items: center;
        span {
            color: rgba(29, 29, 29, 0.5);

            /* text-medium */
            font-family: Inter;
            font-size: 16px;
            font-style: normal;
            font-weight: 400;
            line-height: 24px; /* 150% */
        }
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
