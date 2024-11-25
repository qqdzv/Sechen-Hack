<template>
    <main class="home">
        <section class="banners">
            <CustomInput v-model="user.first_name" label-txt="Имя" typeInp="text" />
            <CustomInput v-model="user.last_name" label-txt="Фамилия" typeInp="text" />
            <CustomInput v-model="user.email" label-txt="Почта" typeInp="text" />
            <CustomDropDown v-model="user.gender" :options="options" placeholder="Пол" text="Пол" />
            <CustomInput v-model="user.age" label-txt="Возраст" typeInp="text" />
            <CustomInput v-model="user.university" label-txt="Университет" typeInp="text" v-if="!isPatient" />
            <CustomInput v-model="user.experience_age" label-txt="Стаж" typeInp="text" v-if="!isPatient" />
            <CustomInput v-model="user.speciality" label-txt="Специализация" typeInp="text" v-if="!isPatient" />
            {{ resp }}
            <MainButton text="Сохранить" @click="saveUser" type="primary" style="width: 100%" />
        </section>
    </main>
</template>

<script setup lang="ts">
import api from '@/axios/api';
import { Doctor, Patient, useUserStore } from '@/store/useUserStore';
import CustomDropDown from '@/ui/CustomDropDown.vue';
import CustomInput from '@/ui/CustomInput.vue';
import MainButton from '@/ui/MainButton.vue';
import { ref, toRaw } from 'vue';

defineOptions({
    name: 'SettingsPage',
});

// Создаем копию пользователя с начальными значениями
const storeUser = useUserStore().user;
const resp = ref('');
const isPatient = (storeUser as Patient).skin_type !== undefined; // Check if user is a Patient

const user = ref({
    first_name: storeUser?.first_name || '',
    last_name: storeUser?.last_name || '',
    email: storeUser?.email || '',
    gender: storeUser?.gender || '',
    age: storeUser?.age || '',
    skin_type: isPatient ? storeUser?.skin_type || '' : '', // Only if user is a Patient
    role: storeUser?.role || '',
    experience_age: storeUser?.experience_age || '',
    university: storeUser?.university || '',
    speciality: storeUser?.speciality || '',
});

const options = ['Мужской', 'Женский'];

interface UserPayload {
    first_name: string;
    last_name: string;
    email: string;
    gender: string;
    age: string;
    skin_type?: string; // Make this optional to prevent issues
}
interface ResponseData {
    detail: string;
}
const updateProfile = async () => {
    let response;
    if (user.value.role === 'user') {
        const payload = {
            ...user.value,
            skin_type: user.value.skin_type || '', // Ensure skin_type is sent as a string
        };
        response = await api.postData<UserPayload, ResponseData>('/user/update_profile', toRaw(payload));
    } else {
        response = await api.postData<UserPayload, ResponseData>('/doctor/update_profile', user.value);
    }

    if (response) {
        resp.value = response.detail; // Assuming `detail` is the desired string
    }
};

const saveUser = () => {
    if (user.value.first_name && user.value.last_name && user.value.email && user.value.gender && user.value.age) {
        if (user.value.gender === 'Мужской') {
            user.value.gender = 'male';
        } else {
            user.value.gender = 'female';
        }

        updateProfile();
    }
};
</script>

<style lang="scss" scoped>
.home {
    width: 100%;
    height: 100%;
    .banners {
        display: flex;
        flex-direction: column;
        gap: 12px;
        width: 100%;
        height: auto;
        overflow-y: scroll;
        padding-bottom: 72px;
    }
}
</style>
