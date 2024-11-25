<template>
    <div class="error-page">
        <h1>Ошибка 404</h1>
        <p>Страница не найдена.</p>
        <button @click="goBack">Вернуться назад</button>
    </div>
</template>

<script setup lang="ts">
const goBack = () => {
    window.history.back();
};
</script>

<style scoped lang="scss">
.error-page {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    height: 100vh; /* Полная высота экрана */
    text-align: center;
    color: var(--color-main);
    font-family: var(--font-main);
    h1 {
        font-size: 2rem;
        margin-bottom: 16px;
    }

    p {
        margin-bottom: 24px;
    }

    button {
        padding: 10px 20px;
        font-size: 1rem;
        cursor: pointer;
        background-color: #1c274c;
        color: white;
        border: none;
        border-radius: 5px;
        transition: background-color 0.3s ease;

        &:hover {
            background-color: #16203c; /* Темнее при наведении */
        }
    }
}
</style>
