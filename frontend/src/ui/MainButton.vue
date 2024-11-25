<template>
    <button :class="[buttonClass, className]" :style="{ width: `${width}px` }">
        <CustomIcon v-if="icon" :id="icon" :width="20" :height="20" className="icon" />
        <div :class="['btn_inner', innerClass]">{{ text }}</div>
    </button>
</template>

<script setup lang="ts">
import { computed } from 'vue';
import CustomIcon from './CustomIcon.vue';

defineOptions({
    name: 'MainButton',
});

const { text, type, width, className, icon } = withDefaults(
    defineProps<{
        text: string;
        type?: 'primary' | 'secondary' | 'base';
        width?: number; // Уточняем типы для type
        className?: string;
        icon?: string;
        innerClass?: string;
    }>(),
    {
        text: '',
        type: 'base',
    },
);

// Вычисляемый класс кнопки
const buttonClass = computed(() => {
    return {
        btn: type === 'base',
        'btn--primary': type === 'primary',
        'btn--secondary': type === 'secondary',
    };
});
</script>

<style lang="scss" scoped>
.btn {
    display: flex;
    min-width: 116px;
    height: 48px;
    padding: 0px 24px;
    justify-content: center;
    align-items: center;
    gap: 8px;
    flex-shrink: 0;
    border-radius: 12px;
    border: 1px solid #efefef;

    color: var(--main-color, #418af9);
    font-family: var(--font-main);
    font-size: 16px;
    font-style: normal;
    font-weight: 700;
    line-height: 24px; /* 150% */
    .btn_inner {
        display: flex;
        justify-content: center;
        align-items: center;
    }
}

.btn--primary {
    display: flex;
    min-width: 116px;
    height: 48px;
    padding: 0px 24px;
    justify-content: center;
    align-items: center;
    gap: 8px;
    flex-shrink: 0;
    border-radius: 12px;
    border: 1px solid #efefef;

    background-color: var(--main-color, #418af9);
    color: #fff;
    font-family: var(--font-main);
    font-size: 16px;
    font-style: normal;
    font-weight: 700;
    line-height: 24px; /* 150% */
    .btn_inner {
        display: flex;
        justify-content: center;
        align-items: center;
    }
}
.btn--secondary {
    display: flex;
    min-width: 116px;
    height: 48px;
    padding: 0px 24px;
    justify-content: center;
    align-items: center;
    gap: 8px;
    flex-shrink: 0;
    border-radius: 12px;
    border: 1px solid #efefef;

    color: var(--main-color, #418af9);
    background-color: #ede8fd;
    font-family: var(--font-main);
    font-size: 16px;
    font-style: normal;
    font-weight: 700;
    line-height: 24px; /* 150% */
    .btn_inner {
        display: flex;
        justify-content: center;
        align-items: center;
    }
}
</style>
