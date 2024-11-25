<template>
    <svg :class="className" :width="width" :height="height">
        <use :href="`/img/iconss.svg#${id}`" :xlinkHref="`/img/icons.svg#${id}`" />
    </svg>
</template>
<script setup lang="ts">
defineOptions({
    name: 'CustomIcon',
});
withDefaults(
    defineProps<{
        id: string;
        width: number;
        height: number;
        className?: string;
    }>(),
    {
        className: '',
    },
);
</script>
