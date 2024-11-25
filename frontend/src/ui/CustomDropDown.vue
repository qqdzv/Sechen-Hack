<template>
    <div class="custom-select">
        <div class="labelWrapper">
            <label>{{ text }}</label>
        </div>
        <div class="custom-dropdown" @click="toggleDropdown">
            <div class="selected">{{ modelValue || placeholder }}</div>
            <div v-if="isOpen" class="options">
                <div v-for="option in options" :key="option" class="option" @click.stop="selectOption(option)">
                    {{ option }}
                </div>
            </div>
            <CustomIcon id="dropDown_arrow" :width="24" :height="24" class="arrow" />
        </div>
    </div>
</template>

<script setup lang="ts">
import { ref, defineEmits, defineProps, watch } from 'vue';
import CustomIcon from './CustomIcon.vue';

const props = defineProps<{
    options: string[]; // Убедитесь, что это строковый массив
    placeholder: string;
    modelValue: string;
    text: string;
}>();

const emit = defineEmits(['update:modelValue']);

const isOpen = ref(false);

const toggleDropdown = () => {
    isOpen.value = !isOpen.value;
};

const selectOption = (option: string) => {
    emit('update:modelValue', option); // Обновляем значение родителя
    isOpen.value = false;
};
</script>
<style scoped>
.custom-dropdown {
    position: relative;
    cursor: pointer;
    border-bottom: 1px solid #d4d4d8;
    border-radius: 4px;
    font-size: 16px;
    transition: border-color 0.3s;
    font-family: var(--font-main);
    z-index: 2;
    width: 100%;
}
.custom-select {
    display: flex;
    width: 100%;
    min-width: 116px;
    flex-direction: column;
    align-items: flex-start;
}

.custom-select:hover {
    border-color: #aaa; /* Цвет границы при наведении */
}
.labelWrapper {
    display: flex;
    padding: 0px 8px 12px 0px;
    align-items: center;
    align-self: stretch;
    flex-direction: row;
    label {
        color: #767676;

        /* text-tiny */
        font-family: Inter;
        font-size: 12px;
        font-style: normal;
        font-weight: 400;
        line-height: 16px; /* 133.333% */
    }
}
.selected {
    padding: 10px;
}

.options {
    position: absolute;
    top: 100%; /* Расположение выпадающего списка */
    left: 0;
    right: 0;
    border: 1px solid #ccc;
    border-radius: 4px;
    background-color: white;

    max-height: 200px; /* Ограничение высоты выпадающего списка */
    overflow-y: auto; /* Прокрутка при переполнении */
    z-index: 100;
}

.option {
    padding: 10px;
    cursor: pointer;
}

.option:hover {
    background-color: #f0f0f0; /* Цвет при наведении на вариант */
}
.arrow {
    position: absolute;
    right: 10px;
    bottom: 10px;
    z-index: 3;
}
span {
    position: absolute;
    top: -30px;
}
</style>
