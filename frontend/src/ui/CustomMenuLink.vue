<template>
    <router-link :to="to" :class="['link', isActive && 'active']" v-bind="filteredProps">
        <CustomIcon :class="icon" :id="icon" :width="32" :height="32" />
        <span :class="'text'">{{ text }}</span>
    </router-link>
</template>

<script setup lang="ts">
import { computed, defineProps, toRefs } from 'vue';
import { useRoute } from 'vue-router';
import CustomIcon from '@/ui/CustomIcon.vue';
import { useRoleStore } from '@/store/useRoleStore';

interface LinkProps {
    icon: string;
    text?: string;
    to: string;
}

const props = defineProps<LinkProps>();
const { to, icon, text } = toRefs(props);
const roleStore = useRoleStore();
// Filter out props for the router link
const filteredProps = computed(() => {
    const { to, icon, text, ...rest } = props; // Exclude `to`, `icon`, and `text` from `props`
    return rest;
});

// Check if the current route matches the link's target
const route = useRoute();
const isActive = computed(() => route.path.includes(to.value));
</script>

<style scoped lang="scss">
.link {
    width: 49px;
    height: 49px;
    display: flex;
    flex-direction: column;
    gap: 2px;
    color: rgba(28, 39, 76, 0.5); /* Default color for the link */
    align-items: center;
    user-select: none;
    outline: none;
    --webkit-tap-highlight-color: transparent;
    --webkit-user-select: none;
    --moz-user-select: none;
    --ms-user-select: none;
    --o-user-select: none;
    --user-select: none;
    cursor: pointer;
    &:focus,
    &:active {
        background-color: transparent;
        outline: none;
    }
    .active {
        color: #1c274c; /* Active link color */
    }

    .icon {
        display: block;
        transition: color 0.2s ease; /* Transition for color changes */
        /* Ensure icon inherits color from the link */
        color: inherit; /* This ensures the icon uses the link's color */
    }
}
.text {
    font-family: var(--font-main);
    font-weight: 700;
    font-size: 12px;
    line-height: normal;
    transition: color 0.2s ease;
}
.active {
    color: #1c274c; /* Active link color */
}
</style>
