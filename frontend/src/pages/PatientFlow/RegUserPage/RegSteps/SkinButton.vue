<template>
    <button :class="buttonClass">
        <div class="btn_inner">
            {{ text }}
            <div class="skinCircle" :style="`background-color: ${colorC}`"></div>
        </div>
    </button>
</template>

<script setup lang="ts">
import { computed } from 'vue';

defineOptions({
    name: 'MainButton',
});

const { text, type, colorC } = withDefaults(
    defineProps<{
        text: string;
        type?: 'primary' | 'base';
        colorC: string;
    }>(),
    {
        text: '',
        type: 'base',
        colorC: '',
    },
);

// Вычисляемый класс кнопки
const buttonClass = computed(() => {
    return {
        btn: type === 'base',
        'btn--primary': type === 'primary',
    };
});
</script>

<style lang="scss">
.btn {
    display: flex;
    width: 112px;
    height: 40px;
    padding: 0px 6px 0 24px;
    align-items: center;
    gap: 8px;
    flex-shrink: 0;
    background-color: #fff;

    color: var(--color-text, #1d1d1d);
    font-family: var(--font-main);
    font-size: 16px;
    font-style: normal;
    font-weight: 700;
    line-height: 24px; /* 150% */
    border-radius: 9999px;
    border: 1px solid #efefef;
    .btn_inner {
        display: flex;
        justify-content: space-between;
        align-items: center;
        width: 100%;
        .skinCircle {
            width: 28px;
            height: 28px;
            flex-shrink: 0;
            border: 1px solid var(--Mian, rgba(29, 29, 29, 0.05));
            border-radius: 50%;
        }
    }
}

.btn--primary {
    display: flex;
    width: 112px;
    height: 40px;
    padding: 0px 6px 0 24px;
    align-items: center;
    gap: 8px;
    flex-shrink: 0;
    background-color: #eff6fb;
    color: var(--color-text, #1d1d1d);
    font-family: var(--font-main);
    font-size: 16px;
    font-style: normal;
    font-weight: 700;
    line-height: 24px; /* 150% */
    border-radius: 9999px;
    border: 1px solid #efefef;
    .btn_inner {
        display: flex;
        justify-content: space-between;
        align-items: center;
        width: 100%;
        .skinCircle {
            width: 28px;
            height: 28px;
            flex-shrink: 0;
            border: 1px solid var(--Mian, rgba(29, 29, 29, 0.05));
            border-radius: 50%;
        }
    }
}
</style>
