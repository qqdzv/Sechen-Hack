<template>
    <div class="aiChatPage">
        <header class="chatHeader">
            <CustomIcon id="arrow_left" :width="24" :height="24" @click="goBack" className="icon" />
            <div class="headerText">
                <h4>Skin GPT</h4>
                <p>Умный помощник</p>
            </div>
        </header>
        <main class="chatBody">
            <div v-for="(message, index) in messages" :key="index" :class="['message', { 'message-user': message.sender === 'user', 'message-bot': message.sender === 'bot' }]">
                {{ message.text }}

                <span :class="['time', { 'time-user': message.sender === 'user', 'time-bot': message.sender === 'bot' }]">
                    {{ message.created_at ? formatDate(message.created_at).time : '' }}
                </span>
            </div>
        </main>
        <div class="inputBar">
            <CustomIcon id="file" :width="32" :height="32" className="fileIcon" />
            <textarea type="text" placeholder="Сообщение" @keyup.enter="sendMessage" @input="autoResize" v-model="newMessage"></textarea>
            <CustomIcon id="send" :width="32" :height="32" className="sendIcon" @click="sendMessage" />
        </div>
    </div>
</template>
<script setup lang="ts">
import api from '@/axios/api';
import CustomIcon from '@/ui/CustomIcon.vue';
import { formatDate } from '@/utils/fortmatDate';
import { ref, onMounted, onBeforeUnmount, Ref } from 'vue';
import { useRouter } from 'vue-router';
defineOptions({
    name: 'MainPatientPage',
});
interface ChatMessage {
    sender: 'user' | 'bot';
    text?: string;
    image?: string;
    created_at?: string;
}
interface AiMessage {
    id: number;
    sender_id: number;
    content: string;
    ai_answer: string;
    role: string;
    created_at: string;
}

const newMessage = ref('');
const messages: Ref<ChatMessage[]> = ref([]);

const getMessages = async () => {
    try {
        const response = await api.getData<AiMessage[]>('/ai_chat/get_history');
        if (response) {
            for (let i = 0; i < response.length; i++) {
                const messagePair = response[i];
                const userMessage: ChatMessage = {
                    sender: 'user',
                    text: messagePair.content, // Используем обработанный текст
                    created_at: new Date(new Date(messagePair.created_at).getTime() + 3 * 60 * 60 * 1000).toISOString(),
                };
                messages.value.push(userMessage);
                const botMessage: ChatMessage = {
                    sender: 'bot',
                    text: messagePair.ai_answer, // Используем обработанный текст
                    created_at: new Date(new Date(messagePair.created_at).getTime() + 3 * 60 * 60 * 1000).toISOString(),
                };
                messages.value.push(botMessage);
            }
        }
    } catch (error) {
        console.error('Ошибка при получении сообщений:', error);
    }
};

// Функция для отправки нового сообщения
const sendMessage = async () => {
    if (!newMessage.value.trim()) return; // Проверка, что сообщение не пустое

    const userMessage: ChatMessage = { sender: 'user', text: newMessage.value, created_at: new Date().toUTCString() };
    // Добавляем сообщение пользователя в чат (локально)
    messages.value.push(userMessage);
    console.log(newMessage.value);
    try {
        // Отправка сообщения на сервер
        const response = await api.postData<{ content: string }, AiMessage>('/ai_chat/send', { content: newMessage.value });

        const botMessage: ChatMessage = {
            sender: 'bot',
            text: response.ai_answer, // Используем обработанный текст
            created_at: new Date(new Date(response.created_at).getTime() + 3 * 60 * 60 * 1000).toISOString(),
        };
        messages.value.push(botMessage);
    } catch (error) {
        console.error('Ошибка при отправке сообщения:', error);
    } finally {
        // Очистка поля ввода
        newMessage.value = '';
    }
};
onMounted(getMessages);
function goBack() {
    router.go(-1);
}
const autoResize = (event: Event) => {
    const textarea = event.target as HTMLTextAreaElement;
    textarea.style.height = '31px'; // Сбрасываем высоту
    textarea.style.height = `${Math.min(textarea.scrollHeight, 110)}px`; // Устанавливаем высоту в зависимости от содержимого
};
const router = useRouter();
</script>
<style lang="scss" scoped>
.aiChatPage {
    display: flex;
    flex-direction: column;
}
.chatHeader {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 60px;
    background: #fff;
    display: flex;
    flex-direction: row;
    align-items: center;
    justify-content: center;
    padding: 0 20px;
    font-family: var(--font-main);
    z-index: 2;
    .icon {
        position: absolute;
        left: 20px;
        top: 50%;
        transform: translateY(-50%);
    }
    .headerText {
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 0;
        h4 {
            color: var(--Text, #1d1d1d);
            font-size: 18px;
            font-style: normal;
            font-weight: 800;
            line-height: normal;
        }
        p {
            color: rgba(29, 29, 29, 0.5);
            text-align: center;
            font-size: 14px;
            font-style: normal;
            font-weight: 500;
            line-height: normal;
        }
    }
}
.inputBar {
    position: fixed;
    bottom: 0;
    left: 0;
    z-index: 2;
    width: 100%;
    height: auto;
    max-height: 130px;
    padding: 8px 20px 15px 20px;

    display: flex;
    flex-direction: row;
    justify-content: space-between;
    align-items: end;
    background: #fff;

    textarea {
        width: 80%;
        border-radius: 12px;
        background: #f0f0f0;
        padding: 8px 12px;
        min-height: 31px;
        max-height: 110px;
        color: var(--Text, #1d1d1d);
        font-family: var(--font-main);
        font-size: 16px;
        font-style: normal;
        font-weight: 400;
        line-height: normal;
        resize: none; /* Отключает возможность изменения размера вручную */
        overflow: hidden; /* Скрываем прокрутку */
        height: 10px;
        &:focus {
            outline: none;
        }
    }
}

.chatBody {
    z-index: 1;
    width: 100%;
    height: auto;
    padding: 70px 10px 90px 10px;
    overflow-y: auto;

    flex-grow: 1;
    display: flex;
    flex-direction: column;
    font-family: var(--font-main);
    justify-content: flex-end;
    gap: 10px;
    .message {
        display: inline-flex;
        max-width: 80%;
        width: auto;
        overflow-y: scroll;
        padding: 12px 16px;
        align-items: center;
        gap: 10px;
        flex-shrink: 0;
        border-radius: 16px;

        margin-bottom: 10px; /* Пространство между сообщениями */
        z-index: 3;
        backdrop-filter: blur(8px);
        overflow: visible;
        .time {
            color: rgba(29, 29, 29, 0.3);
            font-family: var(--font-main);
            font-size: 12px;
            font-style: normal;
            font-weight: 700;
            line-height: normal;
            z-index: 3;
        }
        .time-bot {
            position: absolute;
            bottom: -20px;
            left: 0;
        }
        .time-user {
            position: absolute;
            bottom: -20px;
            right: 0;
        }
    }
    .message-user {
        align-self: flex-end; /* Сообщения пользователя справа */
        text-align: right;
        color: #fff;
        border-radius: 16px;
        background: var(--color-main); /* Светлый синий фон для сообщений пользователя */
        border-radius: 30px 0 30px 30px;
    }

    .message-bot {
        align-self: flex-start; /* Сообщения бота слева */
        text-align: left;
        color: #1d1d1d;
        background: #e9e9e9;
        font-size: 16px;
        font-style: normal;
        font-weight: 400;
        line-height: 150%;
        border-radius: 0 30px 30px 30px;
    }
}
</style>
