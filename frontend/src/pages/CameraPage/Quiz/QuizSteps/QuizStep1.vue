<template>
    <div class="quiz-step1">
        <div class="quiz-step1_header">
            <p class="currentStep">{{ step }}/2</p>
        </div>
        <h3>Какой из этих признаков может указывать на потенциально опасное новообразование?</h3>
        <div class="groupBtns">
            <MainButton text="Ровные, четкие края родинки" type="base" className="quizBtn" innerClass="quizBtn_inner" :class="getButtonClass('Ровные, четкие края родинки')" @click="selectAnswer('Ровные, четкие края родинки')" />
            <MainButton text="Изменение размера за короткий срок" type="base" className="quizBtn" innerClass="quizBtn_inner" :class="getButtonClass('Изменение размера за короткий срок')" @click="selectAnswer('Изменение размера за короткий срок')" />
            <MainButton text="Родинка одного цвета" type="base" className="quizBtn" innerClass="quizBtn_inner" :class="getButtonClass('Родинка одного цвета')" @click="selectAnswer('Родинка одного цвета')" />
            <MainButton text="Родинка с волосками" type="base" className="quizBtn" innerClass="quizBtn_inner" :class="getButtonClass('Родинка с волосками')" @click="selectAnswer('Родинка с волосками')" />
        </div>
        <div class="hideBlock" v-if="selectedOption">
            <MainButton text="Далее" @click="emit('next-step')" type="primary" style="width: 100%" />
            <p>
                <b>Правильный ответ:</b> <i>{{ correctAnswer }}</i>
            </p>
            <p>
                <b>Пояснение:</b> <i>{{ explanation }}</i>
            </p>
        </div>
    </div>
</template>

<script setup lang="ts">
import MainButton from '@/ui/MainButton.vue';
import { ref, computed, watch } from 'vue';

const props = defineProps<{ step?: number }>();
const emit = defineEmits(['next-step']);
const selectedOption = ref<string | null>(null);

// Correct answer and explanation
const correctAnswer = 'Изменение размера за короткий срок';
const explanation = 'Быстрые изменения в родинке, такие как увеличение, неровные края или неоднородный цвет, могут указывать на возможное злокачественное новообразование.';

const selectAnswer = (option: string) => {
    selectedOption.value = option;
};

// Computed property to get button class
const getButtonClass = (option: string) => {
    if (selectedOption.value === null) return ''; // No selection
    if (option === correctAnswer) {
        return 'correct-answer'; // Highlight if it's the correct answer
    } else if (selectedOption.value === option) {
        return 'incorrect-answer'; // Highlight if it's the selected option but incorrect
    }
    return ''; // Default case
};

// Watcher to trigger recalculation of button classes when selectedOption changes
watch(selectedOption, (newValue, oldValue) => {
    console.log('Selected option changed from:', oldValue, 'to:', newValue);
});
</script>

<style lang="scss">
.quiz-step1 {
    display: flex;
    height: 100%;
    flex-direction: column;
    justify-content: space-between;
    border-radius: 24px;
    background-color: var(--bg-1);
    padding: 28px;
    font-family: var(--font-main);
    .quiz-step1_header {
        display: flex;
        justify-content: end;
        color: var(--color-main);
        font-size: 16px;
        font-weight: 700;
        line-height: normal;
    }
    h3 {
        color: #000;
        font-size: 16px;
        font-weight: 700;
        line-height: normal;
    }
    .groupBtns {
        display: flex;
        flex-direction: column;
        gap: 10px;
        .quizBtn {
            width: 100%;
            &.correct-answer {
                background-color: #a2ffa5; /* Change to your desired color */
                color: white; /* Optional: Change text color for visibility */
            }
            &.incorrect-answer {
                background-color: #ffa2a3; /* Change to your desired color */
                color: white; /* Optional: Change text color for visibility */
            }
            .quizBtn_inner {
                color: #1d1d1d;
            }
        }
    }
}
</style>
