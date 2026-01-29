<template>
  <div class="settings-container">
    <h2>设置</h2>

    <!-- 通用设置 -->
    <section class="setting-group">
      <h3>通用设置</h3>
      <div class="setting-item">
        <label>语言</label>
        <select v-model="settings.language">
          <option value="zh-CN">简体中文</option>
          <option value="en-US">English</option>
        </select>
      </div>
      <div class="setting-item">
        <label>主题</label>
        <select v-model="settings.theme">
          <option value="light">浅色</option>
          <option value="dark">深色</option>
          <option value="auto">跟随系统</option>
        </select>
      </div>
    </section>

    <!-- 通知设置 -->
    <section class="setting-group">
      <h3>通知设置</h3>
      <div class="setting-item">
        <label>启用通知</label>
        <input type="checkbox" v-model="settings.notifications.enabled" />
      </div>
      <div class="setting-item" v-if="settings.notifications.enabled">
        <label>声音提醒</label>
        <input type="checkbox" v-model="settings.notifications.sound" />
      </div>
    </section>

    <!-- 账号设置 -->
    <section class="setting-group">
      <h3>账号设置</h3>
      <div class="setting-item">
        <label>用户名</label>
        <input type="text" v-model="settings.account.username" />
      </div>
      <div class="setting-item">
        <label>邮箱</label>
        <input type="email" v-model="settings.account.email" />
      </div>
      <button @click="saveSettings">保存设置</button>
    </section>
  </div>
</template>

<script setup>
import { reactive } from 'vue'

// 设置数据
const settings = reactive({
  language: 'zh-CN',
  theme: 'auto',
  notifications: {
    enabled: true,
    sound: true
  },
  account: {
    username: '',
    email: ''
  }
})

// 保存设置
function saveSettings() {
  // 这里可以调用 API 保存设置
  console.log('保存设置:', settings)
  alert('设置已保存')
}
</script>

<style scoped>
.settings-container {
  max-width: 600px;
  margin: 0 auto;
  padding: 20px;
}
.setting-group {
  margin-bottom: 30px;
}
.setting-group h3 {
  margin-bottom: 10px;
}
.setting-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
}
button {
  margin-top: 10px;
  padding: 8px 16px;
}
</style>
