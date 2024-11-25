<template>
    <div class="quiz-step2">
        <div class="quiz-step2_header">
            <p class="currentStep">{{ step }}/2</p>
        </div>
        <h3>
            Когда лучше всего наносить солнцезащитный крем <br />
            для максимальной защиты?
        </h3>
        <div class="groupBtns">
            <MainButton text="Сразу после того, как выйду на солнце" type="base" className="quizBtn" innerClass="quizBtn_inner" :class="getButtonClass('Сразу после того, как выйду на солнце')" @click="selectAnswer('Сразу после того, как выйду на солнце')" />
            <MainButton text="За 15–30 минут до выхода на улицу" type="base" className="quizBtn" innerClass="quizBtn_inner" :class="getButtonClass('За 15–30 минут до выхода на улицу')" @click="selectAnswer('За 15–30 минут до выхода на улицу')" />
            <MainButton text="Только если солнце светит очень ярко" type="base" className="quizBtn" innerClass="quizBtn_inner" :class="getButtonClass('Только если солнце светит очень ярко')" @click="selectAnswer('Только если солнце светит очень ярко')" />
            <MainButton text="После пребывания на солнце" type="base" className="quizBtn" innerClass="quizBtn_inner" :class="getButtonClass('После пребывания на солнце')" @click="selectAnswer('После пребывания на солнце')" />
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
const correctAnswer = 'За 15–30 минут до выхода на улицу';
const explanation = 'Наносить солнцезащитный крем лучше заранее, чтобы он успел впитаться и начать действовать. Это обеспечивает защиту с момента выхода на солнце и снижает риск повреждения кожи.';

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

<style lang="scss" >
.quiz-step2 {
    display: flex;
    height: 100%;
    flex-direction: column;
    justify-content: space-between;
    border-radius: 24px;
    background-color: var(--bg-1);
    padding: 28px;
    font-family: var(--font-main);
    .quiz-step2_header {
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
