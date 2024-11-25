<template>
    <div class="step7">
        <h2>Как часто вы находитесь под прямыми солнечными лучами?</h2>
        <div class="groupBtns">
            <MainButton text="Ежедневно, более 1 часа" @click="selectAnswer('Ежедневно, более 1 часа')" :key="task7Value === 'Ежедневно, более 1 часа' ? 'male-button' : 'base-male'" :type="task7Value === 'Ежедневно, более 1 часа' ? 'primary' : 'base'" :style="{ width: '100%' }" />
            <MainButton text="Несколько раз в неделю" @click="selectAnswer('Несколько раз в неделю')" :key="task7Value === 'Несколько раз в неделю' ? 'male-button' : 'base-male'" :type="task7Value === 'Несколько раз в неделю' ? 'primary' : 'base'" :style="{ width: '100%' }" />
            <MainButton
                text="Редко, несколько раз в месяц"
                @click="selectAnswer('Редко, несколько раз в месяц')"
                :key="task7Value === 'Редко, несколько раз в месяц' ? 'male-button' : 'base-male'"
                :type="task7Value === 'Редко, несколько раз в месяц' ? 'primary' : 'base'"
                :style="{ width: '100%' }"
            />
            <MainButton
                text="Я использую защитную одежду или SPF"
                @click="selectAnswer('Я использую защитную одежду или SPF')"
                :key="task7Value === 'Я использую защитную одежду или SPF' ? 'male-button' : 'base-male'"
                :type="task7Value === 'Я использую защитную одежду или SPF' ? 'primary' : 'base'"
                :style="{ width: '100%' }"
            />
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
    name: 'TestStep7',
});

const props = defineProps<{ task5?: string }>();
const emit = defineEmits(['next-step', 'update:task7', 'prev-step']);
const task7Value = ref(props.task5 || '');

watch(task7Value, (newAnswer) => {
    emit('update:task7', newAnswer);
});

const selectAnswer = (task: string) => {
    task7Value.value = task;
};

const nextStep = () => {
    if (task7Value.value) {
        emit('next-step');
    }
};

const prevStep = () => {
    emit('prev-step');
};
</script>

<style lang="scss" scoped>
.step7 {
    display: flex;
    flex-direction: column;
    gap: 28px;
    width: 100%;
    height: 100%;
    .groupBtns {
        display: flex;
        flex-direction: column;
        width: 100%;
        justify-content: space-between;
        row-gap: 10px;
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
