<!-- src/views/HomeView.vue -->
<template>
  <div class="home-container">
    <div class="card">
      <h1 class="title">车辆管理系统</h1>
      <p class="subtitle">请选择操作</p>

      <div class="button-group">
        <el-button
          type="primary"
          size="large"
          class="action-btn"
          @click=" router.push('/register')"
        >
          <User class="icon" />
          <span>注册</span>
        </el-button>

        <el-button
          type="success"
          size="large"
          class="action-btn"
          @click=" router.push('/roles')"
        >
          <Setting class="icon" />
          <span>角色</span>
        </el-button>

        <el-button
          type="warning"
          size="large"
          class="action-btn"
          @click=" router.push('/permissions')"
        >
          <Box class="icon" />
          <span>权限</span>
        </el-button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { User, Setting, Box } from '@element-plus/icons-vue'
import {useRouter} from "vue-router";
const router = useRouter()
</script>

<style scoped>
.home-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background: linear-gradient(135deg, #f5f7fa 0%, #e4edf9 100%);
  padding: 20px;
}

.card {
  background: white;
  border-radius: 16px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
  padding: 40px;
  width: 100%;
  max-width: 500px;
  text-align: center;
}

.title {
  font-size: 28px;
  font-weight: 700;
  color: #1d3b6f;
  margin-bottom: 8px;
}

.subtitle {
  color: #666;
  margin-bottom: 32px;
}

.button-group {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.action-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
  height: 56px;
  font-size: 18px;
  font-weight: 600;
  border-radius: 12px;
  transition: transform 0.2s, box-shadow 0.2s;
}

.action-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15);
}

.icon {
  width: 20px;
  height: 20px;
}

/* 响应式：小屏设备 */
@media (max-width: 480px) {
  .card {
    padding: 30px 20px;
  }
  .title {
    font-size: 24px;
  }
  .action-btn {
    height: 50px;
    font-size: 16px;
  }
}
</style>