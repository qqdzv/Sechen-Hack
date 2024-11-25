<template>
    <div class="custom-input">
        <div class="labelWrapper">
            <label>{{ labelTxt }}</label>
        </div>
        <div class="inpWrapper">
            <input :type="currentType" v-model="modelValue" :value="modelValue" />
            <CustomIcon v-if="typeInp === 'password'" id="eye" :width="24" :height="24" @click="isPasswordVisible ? hidePassword() : showPassword()" />
        </div>
    </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue';
import CustomIcon from './CustomIcon.vue';
defineOptions({
    name: 'InputComp',
});

const props = withDefaults(
    defineProps<{
        labelTxt?: string;
        typeInp?: string;
        modelValue?: string;
    }>(),
    {
        labelTxt: '',
        typeInp: 'text',
    },
);
const emit = defineEmits(['update:modelValue']);

const modelValue = defineModel();
const text = ref('');
const isPasswordVisible = ref(false);
const currentType = computed(() => {
    return isPasswordVisible.value ? 'text' : props.typeInp;
});

// Methods to show/hide password
const showPassword = () => {
    isPasswordVisible.value = true;
};

const hidePassword = () => {
    isPasswordVisible.value = false;
};
</script>

<style scoped lang="scss">
.custom-input {
    display: flex;
    max-width: 400px;
    width: 100%;
    min-width: 116px;
    flex-direction: column;
    align-items: flex-start;
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
    .inpWrapper {
        display: flex;
        min-height: 32px;
        padding: 8px 10px;
        align-items: center;
        align-self: stretch;
        border-bottom: 1px solid var(--colors-base-default-300, #d4d4d8);
        input {
            display: flex;
            padding: 0px 6px 2px 6px;
            flex-direction: column;
            justify-content: center;
            align-items: flex-start;
            width: 100%;
            align-self: stretch;

            color: var(--Text, #1d1d1d);

            /* text-medium */
            font-family: Inter;
            font-size: 16px;
            font-style: normal;
            font-weight: 400;
            line-height: 24px; /* 150% */
        }
    }
}
</style>
