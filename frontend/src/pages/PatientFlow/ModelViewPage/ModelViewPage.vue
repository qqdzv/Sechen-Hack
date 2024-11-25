<template>
    <div ref="sceneContainer" class="scene-container" @click="addMarker"></div>
</template>

<script>
import * as THREE from 'three';
import { GLTFLoader } from 'three/examples/jsm/loaders/GLTFLoader';

export default {
    name: 'SkinPassport',
    data() {
        return {
            scene: null,
            camera: null,
            renderer: null,
            model: null,
            markers: [],
        };
    },
    mounted() {
        this.initScene();
        this.loadModel();
        this.animate = this.animate.bind(this); // Привязка animate к this
        requestAnimationFrame(this.animate);
        window.addEventListener('resize', this.onWindowResize);
    },
    beforeUnmount() {
        window.removeEventListener('resize', this.onWindowResize); // Очистка обработчика событий при уничтожении компонента
    },
    methods: {
        initScene() {
            this.scene = new THREE.Scene();
            this.camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
            this.camera.position.z = 5;

            this.renderer = new THREE.WebGLRenderer({ antialias: true });
            this.renderer.setSize(window.innerWidth, window.innerHeight);
            this.$refs.sceneContainer.appendChild(this.renderer.domElement);

            const light = new THREE.DirectionalLight(0xffffff, 1);
            light.position.set(1, 1, 1).normalize();
            this.scene.add(light);
        },
        loadModel() {
            const loader = new GLTFLoader();
            loader.load('/Person.glb', (gltf) => {
                this.model = gltf.scene;
                this.scene.add(this.model);
            });
        },
        animate() {
            requestAnimationFrame(this.animate); // Функция анимации вызывает саму себя
            if (this.model) this.model.rotation.y += 0.01; // Поворот модели
            this.renderer.render(this.scene, this.camera);
        },
        onWindowResize() {
            this.camera.aspect = window.innerWidth / window.innerHeight;
            this.camera.updateProjectionMatrix();
            this.renderer.setSize(window.innerWidth, window.innerHeight);
        },
        addMarker(event) {
            const rect = this.$refs.sceneContainer.getBoundingClientRect();
            const x = ((event.clientX - rect.left) / rect.width) * 2 - 1;
            const y = -((event.clientY - rect.top) / rect.height) * 2 + 1;

            const vector = new THREE.Vector3(x, y, 0.5).unproject(this.camera);

            const markerGeometry = new THREE.SphereGeometry(0.02, 16, 16);
            const markerMaterial = new THREE.MeshBasicMaterial({
                color: 0xff0000,
            });
            const marker = new THREE.Mesh(markerGeometry, markerMaterial);

            marker.position.copy(vector);
            this.scene.add(marker);
            this.markers.push(marker);
        },
    },
};
</script>

<style scoped>
.scene-container {
    width: 100%;
    height: 100vh;
}
</style>
