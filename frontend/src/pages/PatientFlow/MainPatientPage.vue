<template>
    <main class="home">
        <section class="banners">
            <div class="banner_1">
                <div class="texts">
                    <h3>Сканер рака кожи</h3>
                    <p>Исследуйте свое тело</p>
                </div>
                <MainButton text="Сканировать" type="primary" className="btn_1" icon="scan" @click="router.push('/camera')" />
                <img src="/img/homepage/pic1.png" alt="banner_1" />
            </div>
            <div class="banner_2" v-if="user?.role === 'user'">
                <div class="texts">
                    <h3>{{ testBannerText }}</h3>
                    <p>
                        Он поможет нам делать<br />
                        сканирования более точными
                    </p>
                </div>
                <MainButton :text="testBtn" type="primary" className="btn_2" @click="router.push('/test')" />
                <img src="/img/homepage/pic2.png" alt="banner_1" />
            </div>
            <div class="folders_banners">
                <div class="banner_3" v-if="folders" v-for="folder in folders" :key="folder.id" @click="router.push({ path: `/patient/folder/${folder.id}` })">
                    <div class="texts">
                        <div class="head_texts">
                            <h3>{{ folder.folder_name }}</h3>
                            <p>{{ formatDate(folder.created_at).date }}</p>
                        </div>
                        <span>{{ translateToRus(folder.body_part) }}</span>
                    </div>
                    <CustomIcon id="arrow_right" :width="24" :height="24" className="icon" />
                </div>
            </div>
        </section>
    </main>
</template>
<script setup lang="ts">
import { useScansStore } from '@/store/useScansStore';
import { useUserStore } from '@/store/useUserStore';
import CustomIcon from '@/ui/CustomIcon.vue';
import MainButton from '@/ui/MainButton.vue';
import { formatDate } from '@/utils/fortmatDate';
import { translateToRus } from '@/utils/getRusText';
import { computed, ref } from 'vue';
import { useRouter } from 'vue-router';

defineOptions({
    name: 'MainPatientPage',
});
const user = ref(useUserStore().user);
const hasTest = ref(user.value?.has_test);
let testBannerText = computed(() => !hasTest.value ? 'Пройдите небольшой тест' : 'Вы уже прошли тест!');
let testBtn = ref<string>(hasTest ? 'Пройти заново' : 'Пройти');
const folders = useScansStore().folders;
const router = useRouter();
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
        .folders_banners {
            display: flex;
            flex-direction: column;
            gap: 12px;
        }
        .banner_1 {
            padding: 24px;
            border-radius: 24px;
            background: #e3f2fd;
            display: flex;
            flex-direction: column;
            gap: 16px;
            position: relative;
            overflow: hidden;
            .texts {
                display: flex;
                flex-direction: column;
                gap: 6px;
                h3 {
                    color: var(--Text, #1d1d1d);
                    font-family: var(--font-main);
                    font-size: 20px;
                    font-style: normal;
                    font-weight: 800;
                    line-height: 24px; /* 120% */
                }
                p {
                    color: rgba(29, 29, 29, 0.5);
                    font-family: var(--font-main);
                    font-size: 16px;
                    font-style: normal;
                    font-weight: 700;
                    line-height: 24px; /* 150% */
                }
            }
            img {
                width: 31.7948vw;
                height: 31.7948vw;
                position: absolute;
                bottom: -5px;
                right: -5px;
            }
            .btn_1 {
                display: flex;
                width: 200px;
                height: 48px;
                padding: 0px 24px;
                justify-content: center;
                align-items: center;
                gap: 8px;
                flex-shrink: 0;
                border-radius: 12px;
                background: var(--Main, #418af9);
            }
        }
        .banner_2 {
            padding: 24px;

            border-radius: 24px;
            background: #caffe6;
            display: flex;
            flex-direction: column;
            gap: 16px;
            position: relative;
            overflow: hidden;
            .texts {
                display: flex;
                flex-direction: column;
                gap: 6px;
                h3 {
                    color: var(--Text, #1d1d1d);
                    font-family: var(--font-main);
                    font-size: 20px;
                    font-style: normal;
                    font-weight: 800;
                    line-height: 24px; /* 120% */
                }
                p {
                    color: rgba(29, 29, 29, 0.5);
                    font-family: var(--font-main);
                    font-size: 16px;
                    font-style: normal;
                    font-weight: 700;
                    line-height: 24px; /* 150% */
                }
            }
            img {
                width: 88px;
                height: 88px;
                position: absolute;
                bottom: -2px;
                right: -5px;
            }
            .btn_2 {
                display: flex;
                width: 200px;
                height: 48px;
                padding: 0px 24px;
                justify-content: center;
                align-items: center;
                gap: 8px;
                flex-shrink: 0;
                border-radius: 12px;
                background: #3dbf89;
            }
        }
        .banner_3 {
            padding: 24px;
            border-radius: 24px;
            border: 1px solid rgba(29, 29, 29, 0.1);

            display: flex;
            flex-direction: column;
            gap: 16px;
            position: relative;
            overflow: hidden;
            min-height: 150px;
            .texts {
                display: flex;
                flex-direction: column;
                gap: 8px;
                .head_texts {
                    display: flex;
                    flex-direction: row;
                    justify-content: space-between;
                    h3 {
                        color: var(--Text, #1d1d1d);
                        font-family: var(--font-main);
                        font-size: 20px;
                        font-style: normal;
                        font-weight: 800;
                        line-height: 24px; /* 120% */
                    }
                    p {
                        color: rgba(29, 29, 29, 0.5);
                        font-family: var(--font-main);
                        font-size: 12px;
                        font-style: normal;
                        font-weight: 500;
                        line-height: normal;
                    }
                }

                span {
                    width: fit-content;
                    padding: 8px 12px;
                    height: 31px;
                    flex-shrink: 0;
                    border-radius: 100px;
                    background: var(--color-main, #418af9);
                    color: #fff;
                    font-family: var(--font-main);
                    font-size: 12px;
                    font-style: normal;
                    font-weight: 700;
                    line-height: normal;
                }
            }
            .icon {
                position: absolute;
                bottom: 20px;
                right: 20px;
            }
        }
    }
}
</style>
