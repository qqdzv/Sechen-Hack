import { defineConfig } from 'vite';
import vue from '@vitejs/plugin-vue';
import tsconfigPaths from 'vite-tsconfig-paths';
// https://vite.dev/config/
import path from 'path';
export default defineConfig({
    plugins: [vue(), tsconfigPaths()],
    server: {
        hmr: true,
        watch: {
            usePolling: true,
        },
        host: true,
        strictPort: true,
        port: 8000,
    },
    preview: {
        host: true,
        strictPort: true,
        port: 8080,
    },
    resolve: {
        alias: {
            '@': path.resolve(__dirname, './src'),
        },
    },
});
