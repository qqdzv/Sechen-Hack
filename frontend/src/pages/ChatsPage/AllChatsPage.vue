<template>
    <main class="chatsPage">
        <div class="chatsHeader">
            <h3>{{ isLoading ? 'Загрузка...' : 'Чаты' }}</h3>
            <CustomIcon id="addUser" :width="28" :height="28" @click="router.push('/allDoctors')" v-if="userStore.user?.role !== 'doctor'" />
        </div>

        <div class="search">
            <CustomIcon id="search" :width="24" :height="24" class="searchIcon" v-show="!searchText" />
            <input type="text" placeholder="Поиск" v-model="searchText" />
        </div>

        <div class="chats">
            <!-- Loading Skeletons -->
            <template v-if="isLoading">
                <div v-for="n in 6" :key="n" class="skeleton-chat">
                    <div class="skeleton skeleton-profile"></div>
                    <div class="skeleton-text">
                        <div class="skeleton skeleton-text-line"></div>
                        <div class="skeleton skeleton-text-line small"></div>
                    </div>
                </div>
            </template>

            <!-- Error Message -->
            <p v-else-if="errorMessage" class="error-message">{{ errorMessage }}</p>

            <!-- Display Chats -->
            <div v-else v-for="chat in filteredChats" :key="chat.receiver_id" class="chat" @click="navigateToChat(chat.receiver_id)">
                <div class="profile">
                    <p class="initials">{{ chat.userInitials }}</p>
                </div>
                <div class="texts">
                    <h3>{{ chat.reciever_name }}</h3>
                    <h4>{{ chat.lastMessage }}</h4>
                </div>
                <div class="date">{{ formatDate(chat.lastMessageDate).time }}</div>
            </div>
        </div>
    </main>
</template>

<script setup lang="ts">
import { computed, onMounted, ref, toRaw } from 'vue';
import { useRouter } from 'vue-router';
import api from '@/axios/api';
import CustomIcon from '@/ui/CustomIcon.vue';
import { formatDate } from '@/utils/fortmatDate';
import { useUserStore, Doctor, Patient } from '@/store/useUserStore';

defineOptions({ name: 'AllChatsPage' });

interface AllChats {
    [receiver_id: number]: Message[];
}

export interface Message {
    id: number;
    sender_id: number;
    sender_type: string;
    receiver_id: number;
    receiver_type: string;
    receiver_name: string;
    content: string;
    created_at: string;
}

const userStore = useUserStore();
const isLoading = ref(true);
const chats = ref<AllChats>({});
const router = useRouter();
const searchText = ref('');
const errorMessage = ref('');
const chatsWithUserDetails = ref<any[]>([]);

const fetchAllChats = async () => {
    try {
        const response = await api.getData<AllChats>('/messages/get_chats');
        chats.value = response;
        await fetchUsersForChats();
    } catch (error) {
        console.error('Error fetching chats:', error);
        errorMessage.value = 'Ошибка при загрузке чатов. Пожалуйста, попробуйте позже.';
    } finally {
        isLoading.value = false;
        Object.entries(chats.value).map(([id, chat]) => {
            console.log(id, chat);
            return [id, chat]; // Массив из [id, chat] для каждой записи
        });
    }
};

const fetchUserById = async (user_id: number) => {
    try {
        const endpoint = userStore.user?.role === 'user' ? `/doctor/get_doctor/${user_id}` : `/user/get_user/${user_id}`;
        const user = await api.getData<Patient | Doctor>(endpoint);
        return user;
    } catch (error) {
        console.error('Error fetching user:', error);
    }
};

// Запрос информации о пользователях для всех чатов
const fetchUsersForChats = async () => {
    const chatsWithDetails = await Promise.all(
        Object.entries(chats.value).map(async ([receiver_id, chat]) => {
            const lastMessage = chat[chat.length - 1];
            const user = await fetchUserById(Number(receiver_id));

            // Инициализация и данные для отображения
            const initials = user ? `${user.first_name.charAt(0).toUpperCase()}${user.last_name.charAt(0).toUpperCase()}` : '';
            return {
                userInitials: initials,
                reciever_name: user ? `${user.first_name} ${user.last_name}` : lastMessage.receiver_name,
                lastMessage: lastMessage.content,
                lastMessageDate: lastMessage.created_at,
                receiver_id: Number(receiver_id),
            };
        }),
    );
    chatsWithUserDetails.value = chatsWithDetails;
};

// Фильтрация чатов по поиску
const filteredChats = computed(() => {
    const search = searchText.value.toLowerCase();
    return chatsWithUserDetails.value.filter((chat) => chat.reciever_name?.toLowerCase().includes(search));
});

const navigateToChat = (chatId: number) => {
    router.push(`/chat/${chatId}`);
    console.log(toRaw(filteredChats));
    
};

onMounted(fetchAllChats);
</script>

<style lang="scss" scoped>
.chatsPage {
    width: 100%;
    height: 100%;
    padding: 10px 20px 72px 20px;
    font-family: var(--font-main);
    display: flex;
    flex-direction: column;
    gap: 20px;
    .chatsHeader {
        display: flex;
        flex-direction: row;
        justify-content: space-between;
        h3 {
            color: var(--Text, #1d1d1d);
            font-family: var(--font-main);
            font-size: 24px;
            font-weight: 800;
        }
    }
    .search {
        width: 100%;
        height: 48px;

        position: relative;

        border-radius: 12px;
        background: #f1f1f2;
        input {
            width: 100%;
            height: 100%;
            border-radius: 12px;
            color: #1d1d1d;
            font-family: var(--font-main);
            font-size: 16px;
            font-style: normal;
            font-weight: 600;
            line-height: normal;
            padding-left: 20px;
        }
        input::placeholder {
            padding-left: 36px;
        }
        .searchIcon {
            position: absolute;
            top: 50%;
            left: 20px;
            transform: translateY(-50%);
        }
    }
    .chats {
        margin-top: 8px;
        display: flex;
        flex-direction: column;
        gap: 12px;
        width: 100%;
        height: auto;
        overflow-y: scroll;
        padding-bottom: 72px;

        .chat,
        .skeleton-chat {
            position: relative;
            display: flex;
            width: 100%;
            height: auto;
            align-items: start;
            flex-direction: row;
            gap: 16px;
        }

        .chat {
            .profile {
                width: 65px;
                height: 65px;
                display: flex;
                justify-content: center;
                align-items: center;
                background-color: #b3b3b3;
                border-radius: 12px;
                .bukv {
                    font-size: 24px;
                    font-weight: 700;
                    color: #020202;
                    opacity: 0.4;
                }
            }
            h3 {
                color: #000;
                font-family: var(--font-main);
                font-size: 20px;
                font-weight: 700;
            }

            h4 {
                display: flex;
                height: 24px;
                gap: 8px;
                align-items: center;
                color: rgba(29, 29, 29, 0.5);
                font-family: var(--font-main);
                font-size: 14px;
                font-weight: 600;
            }

            .date {
                position: absolute;
                right: 5px;
                bottom: 50%;
                transform: translateX(-50%);
                color: rgba(29, 29, 29, 0.3);
                font-family: var(--font-main);
                font-size: 12px;
                font-style: normal;
                font-weight: 700;
                line-height: normal;
            }
        }

        .skeleton {
            background: #e0e0e0;
            border-radius: 4px;
            animation: pulse 1.5s infinite ease-in-out;
        }

        .skeleton-profile {
            width: 75px;
            height: 75px;
            border-radius: 12px;
        }

        .skeleton-text {
            display: flex;
            flex-direction: column;
            gap: 8px;
            width: 70%;

            .skeleton-text-line {
                height: 16px;
                width: 70%;
            }

            .skeleton-text-line.small {
                width: 40%;
            }
        }
    }
}

@keyframes pulse {
    0% {
        opacity: 1;
    }
    50% {
        opacity: 0.4;
    }
    100% {
        opacity: 1;
    }
}
</style>
