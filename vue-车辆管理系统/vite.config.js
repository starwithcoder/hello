import { fileURLToPath, URL } from 'node:url'

import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import vueDevTools from 'vite-plugin-vue-devtools'

import WindiCSS from 'vite-plugin-windicss'
import path from 'path'

// https://vite.dev/config/
export default defineConfig({
  resolve: {
    alias: {
      
      
      '~': path.resolve(__dirname, 'src'),
    }
  },
  plugins: [
    vue(),
    vueDevTools(),
    WindiCSS(),
  ],
  base: './',
 server: {
    port: 3000,
  proxy: {
    '/api': {
      target: 'http://127.0.0.1:5000', // 后端地址
      changeOrigin: true
    }
  }
}

})
