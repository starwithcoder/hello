import { createApp } from 'vue'
import axios from 'axios'

import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import 'virtual:windi.css'

import App from './App.vue'
import router from './router'

const app = createApp(App)

// 配置axios
axios.defaults.baseURL = 'http://192.168.1.6:5000/api' // 设置基础URL

// 请求拦截器
axios.interceptors.request.use(
  config => {
    // 从localStorage获取token
    const token = localStorage.getItem('token')
    if (token) {
      // 设置请求头
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  error => {
    return Promise.reject(error)
  }
)

// 响应拦截器
axios.interceptors.response.use(
  response => {
    return response
  },
  error => {
    // 处理401未授权错误
    if (error.response && error.response.status === 401) {
      // 清除登录状态
      localStorage.removeItem('isLoggedIn')
      localStorage.removeItem('token')
      // 跳转到登录页
      router.push('/login')
    }
    return Promise.reject(error)
  }
)

// 将axios挂载到全局
app.config.globalProperties.$axios = axios

app.use(router)

app.use(ElementPlus)

app.mount('#app')
