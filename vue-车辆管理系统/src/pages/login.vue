<template>
  <div class="login-container" >
    <div class="login-form-wrapper">
      <h2 class="login-title">登录</h2>
      <el-form
        ref="loginFormRef"
        :model="loginForm"
        :rules="loginRules"
        class="login-form"
        label-position="top"
      >
        <el-form-item label="用户名" prop="username">
          <el-input
            v-model="loginForm.username"
            placeholder="请输入用户名"
            prefix-icon="User"
          ></el-input>
        </el-form-item>
        <el-form-item label="密码" prop="password">
          <el-input
            v-model="loginForm.password"
            type="password"
            placeholder="请输入密码"
            prefix-icon="Lock"
            show-password
          ></el-input>
        </el-form-item>
        <el-form-item>
          <el-button  class = 'login_button' type="primary" @click="handleLogin" :loading="loading" block>
            {{ loading ? '登录中...' : '登录' }}
          </el-button>

        </el-form-item>
      </el-form>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'
import { ElMessage } from 'element-plus'

const router = useRouter()
const loginFormRef = ref()
const loading = ref(false)

const loginForm = reactive({
  username: '',
  password: ''
})

const loginRules = {
  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' },
    { min: 3, max: 20, message: '用户名长度在 3 到 20 个字符', trigger: 'blur' }
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { min: 6, max: 20, message: '密码长度在 6 到 20 个字符', trigger: 'blur' }
  ]
}

const handleLogin = async () => {
  if (!loginFormRef.value) return
  
  try {
    await loginFormRef.value.validate()
    loading.value = true
    console.log('登录信息:', loginForm.username, loginForm.password)
    // 发送实际的登录请求到API


    const response = await axios.post('/login', {
      username: loginForm.username,
      password: loginForm.password
    },{
      headers: {
        'Content-Type': 'application/json'
      }
    })

    // 登录成功处理
    if (response.status === 200) {
      ElMessage.success('登录成功')
      localStorage.setItem('isLoggedIn', 'true')
      // 如果API返回了token等信息，可以在这里存储

      if (response.data.token) {
        localStorage.setItem('token', response.data.token)

      }

      router.push('/drivers')
    } else {
      ElMessage.error(response.data.message || '登录失败，请检查账号密码')
    }
  } catch (error) {
    console.error('登录请求失败:', error)
    if (error.response) {
      // 服务器返回了错误状态码
      ElMessage.error(error.response.data.message || '登录失败，请稍后重试')
    } else if (error.request) {
      // 请求已发出但没有收到响应
      ElMessage.error('网络异常，请检查网络连接')
    } else {
      // 请求配置错误
      ElMessage.error('请求错误，请稍后重试')
    }
  } finally {
    loading.value = false
  }
}

const handleRegister = () => {
  router.push('/register')
}
</script>

<style scoped>
.login-container {
  width: 100vw;    /* 必须设宽高 */
  height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background-color: #4886e3;
  background-image: url('../static/imgs/loginbg3.jpg');
  background-size: cover; /* 拉伸/压缩图片，保持比例，完全覆盖容器（超出部分裁剪） */
  background-repeat: no-repeat; /* 禁止图片重复（尺寸不足时默认会重复） */
  background-position: center center; /* 图片居中显示（裁剪时保留中间核心区域） */
}

.login-form-wrapper {
  width: 100%;
  max-width: 400px;
  padding: 30px;
  background-color: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}

.login-title {
  text-align: center;
  margin-bottom: 24px;
  color: #303133;
}

.login-form {
  width: 100%;
}

.login_button{
  width: 100%;
}
</style>