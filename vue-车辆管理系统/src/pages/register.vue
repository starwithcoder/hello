<template>
  <div class="login-container">
    <div class="login-form-wrapper">
      <h2 class="login-title">注册</h2>
      <el-form
        ref="registerFormRef"
        :model="registerForm"
        :rules="registerRules"
        class="login-form"
        label-position="top"
      >
        <el-form-item label="用户名" prop="username">
          <el-input
            v-model="registerForm.username"
            placeholder="请输入用户名"
            prefix-icon="User"
          ></el-input>
        </el-form-item>
      
        <el-form-item label="密码" prop="password">
          <el-input
            v-model="registerForm.password"
            type="password"
            placeholder="请输入密码"
            prefix-icon="Lock"
            show-password
          ></el-input>
        </el-form-item>
        <el-form-item label="确认密码" prop="confirmPassword">
          <el-input
            v-model="registerForm.confirmPassword"
            type="password"
            placeholder="请确认密码"
            prefix-icon="Lock"
            show-password
          ></el-input>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleRegister" :loading="loading" block>
            {{ loading ? '注册中...' : '注册' }}
          </el-button>
        </el-form-item>
      </el-form>
      <div class="register-footer">
        <span>已有账号？</span>
        <el-button type="text" @click="goToLogin">去登录</el-button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'
import { ElMessage } from 'element-plus'

const router = useRouter()
const registerFormRef = ref()
const loading = ref(false)

const registerForm = reactive({
  username: '',
  password: '',
  confirmPassword: ''
})

const registerRules = {
  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' },
    { min: 3, max: 20, message: '用户名长度在 3 到 20 个字符', trigger: 'blur' }
  ],

  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { min: 6, max: 20, message: '密码长度在 6 到 20 个字符', trigger: 'blur' }
  ],
  confirmPassword: [
    { required: true, message: '请确认密码', trigger: 'blur' },
    { 
      validator: (rule, value, callback) => {
        if (value !== registerForm.password) {
          callback(new Error('两次输入密码不一致'))
        } else {
          callback()
        }
      }, 
      trigger: 'blur' 
    }
  ]
}

const handleRegister = async () => {
  if (!registerFormRef.value) return
  
  try {
    await registerFormRef.value.validate()
    loading.value = true
    
    // 发送实际的注册请求到API
    const response = await axios.post('/register', {
      username: registerForm.username,
      password: registerForm.password,
      role: ''
    })
    
    // 注册成功处理
    if (response.data.status === 201) {
      ElMessage.success('注册成功，请登录')
      // 注册成功后跳转到登录页
      router.push('/login')
    } else {
      ElMessage.error(response.data.message || '注册失败，请稍后重试')
    }
  } catch (error) {
    console.error('注册请求失败:', error)
    if (error.response) {
      // 服务器返回了错误状态码
      ElMessage.error(error.response.data.message || '注册失败，请稍后重试')
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

const goToLogin = () => {
  router.push('/login')
}
</script>

<style scoped>
.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background-color: #f5f7fa;
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

.register-footer {
  margin-top: 20px;
  text-align: center;
  color: #606266;
  font-size: 14px;
}

.register-footer .el-button {
  padding: 0;
  margin-left: 8px;
}
</style>