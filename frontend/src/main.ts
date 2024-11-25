import { createApp } from 'vue';
import App from './App.vue';
import { createWebHistory, createRouter } from 'vue-router';
import FormLayout from './layouts/FormLayout.vue';
import LoginUserPage from './pages/PatientFlow/LoginUserPage/LoginUserPage.vue';
import RegUserPage from './pages/PatientFlow/RegUserPage/RegUserPage.vue';
import CameraPage from './pages/CameraPage/CameraPage.vue';
import GlobalAuth from './pages/GlobalAuth.vue';
import { createPinia } from 'pinia';
import LoginDoctorPage from './pages/DoctorFlow/LoginDoctorPage/LoginDoctorPage.vue';
import RegDoctorPage from './pages/DoctorFlow/RegDoctorPage/RegDoctorPage.vue';
import MainLayout from './layouts/MainLayout.vue';
import MainPatientPage from './pages/PatientFlow/MainPatientPage.vue';
import ErrorPage from './pages/ErrorPage.vue';
import TestPage from './pages/PatientFlow/TestPage/TestPage.vue';
import AllChatsPage from './pages/ChatsPage/AllChatsPage.vue';
import ChatPage from './pages/ChatsPage/ChatPage.vue';
import FolderPage from './pages/PatientFlow/FolderPage/FolderPage.vue';
import { useUserStore } from './store/useUserStore';
import { useRoleStore } from './store/useRoleStore';
import HistoryPage from './pages/PatientFlow/HistoryPage/HistoryPage.vue';
import AiChatPage from './pages/AiChatPage/AiChatPage.vue';
import SettingsPage from './pages/SettingsPage/SettingsPage.vue';
import QuizPage from './pages/CameraPage/Quiz/QuizPage.vue';
import ScanReportPage from './pages/ScanReportPage/ScanReportPage.vue';
import AllDoctorsPage from './pages/PatientFlow/AllDoctorsPage/AllDoctorsPage.vue';

const routes = [
    {
        path: '/select',
        component: FormLayout,
        children: [{ path: '', component: GlobalAuth }],
    },
    {
        path: '/login/patient',
        component: FormLayout,
        children: [{ path: '', component: LoginUserPage }],
    },
    {
        path: '/register/patient',
        component: FormLayout,
        children: [{ path: '', component: RegUserPage }],
    },
    {
        path: '/login/doctor',
        component: FormLayout,
        children: [{ path: '', component: LoginDoctorPage }],
    },
    {
        path: '/register/doctor',
        component: FormLayout,
        children: [{ path: '', component: RegDoctorPage }],
    },
    {
        path: '/patient/home',
        component: MainLayout,
        children: [{ path: '', component: MainPatientPage }],
    },
    { path: '/camera', component: CameraPage },
    { path: '/:catchAll(.*)', component: ErrorPage },
    { path: '/test', component: FormLayout, children: [{ path: '', component: TestPage }] },
    { path: '/patient/chats', component: MainLayout, children: [{ path: '', component: AllChatsPage }] },
    { path: '/doctor/chats', component: MainLayout, children: [{ path: '', component: AllChatsPage }] },
    { path: '/chat/:id', component: ChatPage },
    {
        path: '/patient/folder/:id',
        name: 'FolderPage',
        component: MainLayout,
        children: [{ path: '', component: FolderPage }],
    },
    { path: '/patient/history', component: MainLayout, children: [{ path: '', component: HistoryPage }] },
    { path: '/ai_chat', component: MainLayout, children: [{ path: '', component: AiChatPage }] }, 
    { path: '/settings', component: MainLayout, children: [{ path: '', component: SettingsPage }] },
    { path: '/quiz', component: QuizPage },
    { path: '/scanReport', component: ScanReportPage },
    { path: '/allDoctors', component: AllDoctorsPage },
];

const router = createRouter({
    history: createWebHistory(),
    routes,
});
router.beforeEach((to, from, next) => {
    const roleStore = useRoleStore();
    const userRole = roleStore.role;

    // Разрешаем доступ для всех пользователей на страницы логина и регистрации
    const publicPaths = ['/login/patient', '/register/patient', '/login/doctor', '/register/doctor'];
    if (publicPaths.includes(to.path)) {
        return next();
    }

    // Проверка доступа для маршрутов пациентов и докторов
    if (to.path.includes('/patient') && userRole !== 'patient') {
        return next('/error');
    } else if (to.path.includes('/doctor') && userRole !== 'doctor') {
        console.log(to.path.includes('/doctor'));

        return next('/error');
    }

    next(); // Разрешаем доступ, если проверка пройдена
});
const pinia = createPinia();

createApp(App).use(pinia).use(router).mount('#app');
