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

})
