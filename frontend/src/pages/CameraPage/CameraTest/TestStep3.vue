<template>
    <div class="step3">
        <h2>Каков приблизительный размер новообразования?</h2>
        <div class="groupBtns">
            <MainButton
                text="Меньше 5 мм (ластик на карандаше)"
                @click="selectAnswer('Меньше 5 мм (ластик на карандаше)')"
                :key="task3Value === 'Меньше 5 мм (ластик на карандаше)' ? 'male-button' : 'base-male'"
                :type="task3Value === 'Меньше 5 мм (ластик на карандаше)' ? 'primary' : 'base'"
                :style="{ width: '100%' }"
            />
            <MainButton text="От 5 до 10 мм (горошина)" @click="selectAnswer('От 5 до 10 мм (горошина)')" :key="task3Value === 'От 5 до 10 мм (горошина)' ? 'male-button' : 'base-male'" :type="task3Value === 'От 5 до 10 мм (горошина)' ? 'primary' : 'base'" :style="{ width: '100%' }" />
            <MainButton text="Больше 10 мм (монета)" @click="selectAnswer('Больше 10 мм (монета)')" :key="task3Value === 'Больше 10 мм (монета)' ? 'male-button' : 'base-male'" :type="task3Value === 'Больше 10 мм (монета)' ? 'primary' : 'base'" :style="{ width: '100%' }" />
            <MainButton text="Не уверен(а)" @click="selectAnswer('Не уверен(а)')" :key="task3Value === 'Не уверен(а)' ? 'male-button' : 'base-male'" :type="task3Value === 'Не уверен(а)' ? 'primary' : 'base'" :style="{ width: '100%' }" />
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
    name: 'TestStep3',
});

const props = defineProps<{ task3?: string }>();
const emit = defineEmits(['next-step', 'update:task3', 'prev-step']);
const task3Value = ref(props.task3 || '');

watch(task3Value, (newAnswer) => {
    emit('update:task3', newAnswer);
});

const selectAnswer = (task: string) => {
    task3Value.value = task;
};

const nextStep = () => {
    if (task3Value.value) {
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
    gap: 18px;
    width: 100%;
    height: 100%;
    .groupBtns {
        display: flex;
        flex-direction: column;
        width: 100%;
        justify-content: space-between;
        gap: 8px;
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
