<template>
    <div class="step7">
        <h2>
            Спасибо! <br />
            При желании, Вы можете пройти тест заново
        </h2>
    </div>
</template>

<script setup lang="ts">
import { useUserStore } from '@/store/useUserStore';
import { defineEmits, onMounted } from 'vue';
import { useRouter } from 'vue-router';
defineOptions({
    name: 'TestStep8',
});

const router = useRouter();
const emit = defineEmits(['submit']);
const userStore = useUserStore();
onMounted(() => {
    emit('submit');
    setTimeout(() => {
        router.push(`/${userStore.user?.role === 'user' ? 'patient' : 'doctor'}/home`);
    }, 4000);
});
</script>

<style lang="scss" scoped>
.step7 {
    display: flex;
    flex-direction: column;
    gap: 28px;
    width: 100%;
    height: 100%;
    justify-content: center;
    align-items: center;
    h2 {
        color: var(--Text, #1d1d1d);
        font-family: var(--font-main);
        font-size: 32px;
        font-style: normal;
        font-weight: 600;
        line-height: normal;
    }
}
</style>
