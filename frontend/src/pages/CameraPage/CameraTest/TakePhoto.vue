<template>
    <div class="cropPage">
        <div v-if="imageUrl" class="croper">
            <img ref="image" :src="imageUrl" alt="Captured Image" />
        </div>
        <div class="wrapBtn">
            <MainButton @click="cropImage" type="primary" text="Обрезать" :style="{ width: '100%' }" />
        </div>
    </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onBeforeUnmount, nextTick } from 'vue';
import Cropper from 'cropperjs';
import 'cropperjs/dist/cropper.min.css';
import MainButton from '@/ui/MainButton.vue';

const croppedImage = ref<string | null>(null);
const image = ref<HTMLImageElement | null>(null);
let cropper: Cropper | null = null;
const props = defineProps<{ imageUrl?: string }>();
const emit = defineEmits(['submit', 'update:task8']);
const imageUrl = ref(props.imageUrl || '');

onMounted(() => {
    if (image.value) {
        cropper = new Cropper(image.value, {
            aspectRatio: 1,
            viewMode: 2,
            guides: false,
        });
    }
});

const submit = () => {
    emit('submit');
};
const cropImage = () => {
    if (cropper) {
        croppedImage.value = cropper.getCroppedCanvas().toDataURL('image/png');
        emit('update:task8', croppedImage.value);
        emit('submit'); // Emit the cropped image
    }
};

onBeforeUnmount(() => {
    if (cropper) {
        cropper.destroy();
    }
});
</script>

<style lang="scss">
.cropPage {
    width: 100%;
    height: 100dvh;
    background-color: #1d1d1d;
    display: flex;
    flex-direction: column;
    input {
        width: 200px;
        height: 50px;
    }
    button {
        width: 100px;
        height: 20px;
    }

    .croper {
        width: 100%;
        height: 100%;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        border-radius: 20px;
    }
    .wrapBtn {
        position: fixed;
        bottom: 0;
        width: 100%;
        padding: 20px;
    }
}

.cropper-container {
    background-color: rgba(0, 0, 0, 0.6);
}
.cropper-bg {
    background-image: inherit !important;
    background-color: #1d1d1d !important;
}
.cropper-modal {
    background-color: #1d1d1d !important;
    opacity: 0.4;
}
/* Настройка рамки выделенной области */
.cropper-crop-box {
    /* border: 2px solid #ffffff; Белая рамка */
    border-radius: 16% !important;
}
.cropper-view-box {
    background-color: transparent !important;
    outline: none !important;
    border-radius: 16% !important;
}
/* Полупрозрачный слой внутри выделенной области */
.cropper-face {
    background-color: rgba(255, 255, 255, 0.2);
    border-radius: 16%; /* Полупрозрачный белый цвет */
}
.cropper-point {
    background-color: transparent !important;
}
/* Линии по краям выделенной области */
.cropper-line {
    background-color: transparent !important; /* Голубой цвет для границ */
    width: 2px; /* Толщина линий */
}

/* Стайлинг только угловых маркеров */
.cropper-point.point-se, /* Bottom-right */
.cropper-point.point-sw, /* Bottom-left */
.cropper-point.point-ne, /* Top-right */
.cropper-point.point-nw {
    /* Top-left */
    width: 30%;
    height: 30%;
}
.cropper-point.point-se {
    display: inline-block; /* Чтобы элемент имел размеры */
    background-color: #f0f0f0; /* Цвет фона */
    border-bottom: 3px solid #fff;
    border-right: 3px solid #fff; /* Цвет и толщина границы */
    border-radius: 0 0 55% 0;
}
.cropper-point.point-se ::after {
    width: 30%; /* 50% длины */
    height: 30%; /* Высота, равная высоте span */
    background-color: transparent; /* Прозрачный фон */
    border-radius: 0 0 55% 0;
    border-bottom: 3px solid #fff;
    border-right: 3px solid #fff; /* Цвет и толщина границы */
}
.cropper-point.point-sw {
    display: inline-block; /* Чтобы элемент имел размеры */
    background-color: #f0f0f0; /* Цвет фона */
    border-bottom: 3px solid #fff;
    border-left: 3px solid #fff; /* Цвет и толщина границы */
    border-radius: 0 0 0 55%;
}
.cropper-point.point-sw ::after {
    width: 30%; /* 50% длины */
    height: 30%; /* Высота, равная высоте span */
    background-color: transparent; /* Прозрачный фон */
    border-radius: 0 0 0 55%;
    border-bottom: 3px solid #fff;
    border-left: 3px solid #fff; /* Цвет и толщина границы */
}
.cropper-point.point-ne {
    display: inline-block; /* Чтобы элемент имел размеры */
    background-color: #f0f0f0; /* Цвет фона */
    border-top: 3px solid #fff;
    border-right: 3px solid #fff; /* Цвет и толщина границы */
    border-radius: 0 55% 0 0;
}
.cropper-point.point-ne ::after {
    width: 30%; /* 50% длины */
    height: 30%; /* Высота, равная высоте span */
    background-color: transparent; /* Прозрачный фон */
    border-radius: 0 55% 0 0;
    border-top: 3px solid #fff;
    border-right: 3px solid #fff; /* Цвет и толщина границы */
}
.cropper-point.point-nw {
    display: inline-block; /* Чтобы элемент имел размеры */
    background-color: #f0f0f0; /* Цвет фона */
    border-top: 3px solid #fff;
    border-left: 3px solid #fff; /* Цвет и толщина границы */
    border-radius: 55% 0 0 0;
}
.cropper-point.point-nw ::after {
    width: 30%; /* 50% длины */
    height: 30%; /* Высота, равная высоте span */
    background-color: transparent; /* Прозрачный фон */
    border-radius: 55% 0 0 0;
    border-top: 3px solid #fff;
    border-left: 3px solid #fff; /* Цвет и толщина границы */
}
</style>
