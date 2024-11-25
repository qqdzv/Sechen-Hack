<template>
    <div class="step5">
        <h2>
            Есть ли у вас зуд, боль или жжение<br />
            в области родинки?
        </h2>
        <div class="groupBtns">
            <MainButton text="Нет" :key="task5Value === false ? 'male-button' : 'base-male'" @click="selectAnswer(false)" :type="task5Value === false ? 'primary' : 'base'" :width="165" />
            <MainButton text="Да" @click="selectAnswer(true)" :key="task5Value === true ? 'male-button' : 'base-male'" :type="task5Value === true ? 'primary' : 'base'" :width="165" />
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
    name: 'TestStep5',
});

const props = defineProps<{ task5?: boolean }>();
const emit = defineEmits(['next-step', 'update:task5', 'prev-step']);
const task5Value = ref(props.task5 || false);

watch(task5Value, (newAnswer) => {
    emit('update:task5', newAnswer);
});

const selectAnswer = (task: boolean) => {
    task5Value.value = task;
};

const nextStep = () => {
    emit('next-step');
};

const prevStep = () => {
    emit('prev-step');
};
</script>

<style lang="scss" scoped>
.step5 {
    display: flex;
    flex-direction: column;
    gap: 48px;
    width: 100%;
    height: 100%;
    .groupBtns {
        display: flex;
        flex-direction: row;
        width: 100%;
        justify-content: space-between;
        row-gap: 10px;
        flex-wrap: wrap;
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
