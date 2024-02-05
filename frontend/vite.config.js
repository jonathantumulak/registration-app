import { fileURLToPath, URL } from 'node:url'

import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [
    vue(),
  ],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url)),
      vue: 'vue/dist/vue.esm-bundler.js',
      'balm-ui-plus': 'balm-ui/dist/balm-ui-plus.esm.js',
      'balm-ui-css': 'balm-ui/dist/balm-ui.css'
    }
  },
  server: {
    host: '0.0.0.0',
    port: '8080',
    cors: {
      "origin": "*",
      "methods": "GET,PUT,PATCH,POST,DELETE",
      "allowedHeaders": 'X-Requested-With, content-type, Authorization',
    },
  },
})
