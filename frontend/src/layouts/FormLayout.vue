<template>
    <div class="formLayout">
        <CustomIcon id="logo" :width="207" :height="33" className="logo" />
        <router-view />
    </div>
</template>

<script setup lang="ts">
import CustomIcon from '@/ui/CustomIcon.vue';
defineOptions({
    name: 'FormLayout',
});
</script>

<style scoped lang="scss">
.formLayout {
    width: 100%;
    padding-top: 36px;
    display: flex;
    flex-direction: column;
    align-items: center;
    height: 100dvh;
    .logo {
        position: relative;
        width: 207px;
        height: 33px;
        z-index: 6;
    }
}
</style>
