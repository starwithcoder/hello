<template>
  <div class="main-layout">
    <!-- 侧边导航栏 -->
    <Sidebar ref="sidebarRef" />
    
    <!-- 主内容区域 -->
    <div class="main-content">
      <!-- 顶部导航栏 -->
      <header class="top-header">
        <div class="header-left">
          <el-button
            type="text"
            @click="handleToggleSidebar"
            class="header-toggle"
            size="small"
          >
          
          </el-button>
        </div>
        <div class="header-right">
          <el-dropdown trigger="click">
            <span class="user-info">
              <el-avatar :size="32" src="https://xsgames.co/randomusers/avatar.php?g=pixel"></el-avatar>
              <span class="user-name">管理员</span>
              <el-icon :size="16"><ArrowDown /></el-icon>
               
            </span>
            <template #dropdown>
              <el-dropdown-menu>
                <el-dropdown-item>
                  <el-icon><User /></el-icon>
                  <router-link to="/profile">
                    <el-button type="primary" size="small">个人中心</el-button>
                  </router-link>
                </el-dropdown-item>
                <el-dropdown-item>
                  <el-icon><Setting /></el-icon>
                  <router-link to="/settings">
                    <el-button type="primary" size="small">设置</el-button>
                  </router-link>
                </el-dropdown-item>
                <el-dropdown-item divided @click="handleLogout">
                  <el-icon><SwitchButton /></el-icon>
                  <span>退出登录</span>
                </el-dropdown-item>
              </el-dropdown-menu>
            </template>
          </el-dropdown>
        </div>
      </header>
      
      <!-- 页面内容 -->
      <main class="page-content">
        <router-view v-slot="{ Component }">
          <transition name="fade" mode="out-in">
            <component :is="Component" />
          </transition>
        </router-view>
      </main>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { ArrowDown, User, Setting, SwitchButton, Menu } from '@element-plus/icons-vue'
import Sidebar from '../Navigation/Sidebar.vue'

const sidebarRef = ref()
const router = useRouter()

const handleToggleSidebar = () => {
  if (sidebarRef.value) {
    sidebarRef.value.toggleSidebar()
  }
}

// 退出登录处理函数
const handleLogout = () => {
  // 清除登录状态
  localStorage.removeItem('isLoggedIn')
  // 跳转到登录页面
  router.push('/login')
}
</script>





<style scoped>
.main-layout {
  display: flex;
  height: 100vh;
  overflow: hidden;
}

.main-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.top-header {
  height: 60px;
  background-color: #fff;
  border-bottom: 1px solid #ebeef5;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 20px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
}

.header-left {
  display: flex;
  align-items: center;
}

.header-toggle {
  color: #606266;
  margin-right: 20px;
}

.header-right {
  display: flex;
  align-items: center;
}

.user-info {
  display: flex;
  align-items: center;
  cursor: pointer;
  padding: 5px 10px;
  border-radius: 4px;
  transition: background-color 0.3s;
}

.user-info:hover {
  background-color: #f5f7fa;
}

.user-name {
  margin: 0 10px;
  font-size: 14px;
  color: #303133;
}

.page-content {
  flex: 1;
  padding: 20px;
  overflow-y: auto;
  background-color: #f5f7fa;
}

/* 页面切换动画 */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>