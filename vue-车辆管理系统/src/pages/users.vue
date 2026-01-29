<template>
  <div class="users-page">
    <div class="page-header">
      <h1 class="page-title">用户管理</h1>
      <p class="page-subtitle">管理系统用户信息</p>
    </div>
    
    <!-- 搜索和筛选 -->
    <el-card shadow="hover" class="filter-card">
      <el-form :model="searchForm" label-position="left" label-width="80px">
        <el-row :gutter="20">
          <el-col :span="8">
            <el-form-item label="用户名">
              <el-input v-model="searchForm.username" placeholder="请输入用户名"></el-input>
            </el-form-item>
          </el-col>
          <el-col :span="8">
            <el-form-item label="邮箱">
              <el-input v-model="searchForm.email" placeholder="请输入邮箱"></el-input>
            </el-form-item>
          </el-col>
          <el-col :span="8">
            <el-form-item label="状态">
              <el-select v-model="searchForm.status" placeholder="请选择状态">
                <el-option label="全部" value=""></el-option>
                <el-option label="启用" value="active"></el-option>
                <el-option label="禁用" value="inactive"></el-option>
              </el-select>
            </el-form-item>
          </el-col>
        </el-row>
        <div class="filter-actions">
          <el-button type="primary" @click="handleSearch">搜索</el-button>
          <el-button @click="handleReset">重置</el-button>
          <el-button type="success" @click="handleAddUser">新增用户</el-button>
        </div>
      </el-form>
    </el-card>
    
    <!-- 用户列表 -->
    <el-card shadow="hover" class="users-card">
      <template #header>
        <div class="card-header">
          <span>用户列表</span>
          <span class="user-count">(共 {{ filteredUsers.length }} 条记录)</span>
        </div>
      </template>
      <el-table :data="filteredUsers" stripe border style="width: 100%">
        <el-table-column prop="id" label="ID" width="80"></el-table-column>
        <el-table-column prop="avatar" label="头像" width="80">
          <template #default="scope">
            <el-avatar :size="40" :src="scope.row.avatar"></el-avatar>
          </template>
        </el-table-column>
        <el-table-column prop="username" label="用户名" width="150"></el-table-column>
        <el-table-column prop="email" label="邮箱"></el-table-column>
        <el-table-column prop="role" label="角色" width="120">
          <template #default="scope">
            <el-tag :type="scope.row.role === 'admin' ? 'warning' : 'success'">
              {{ scope.row.role === 'admin' ? '管理员' : '普通用户' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="status" label="状态" width="120">
          <template #default="scope">
            <el-switch
              v-model="scope.row.status"
              :active-value="'active'"
              :inactive-value="'inactive'"
              @change="handleStatusChange(scope.row)"
            >
            </el-switch>
          </template>
        </el-table-column>
        <el-table-column prop="createdAt" label="创建时间" width="180"></el-table-column>
        <el-table-column prop="updatedAt" label="更新时间" width="180"></el-table-column>
        <el-table-column label="操作" width="200" fixed="right">
          <template #default="scope">
            <el-button type="primary" size="small" @click="handleEditUser(scope.row)">
              <el-icon><Edit /></el-icon>
              编辑
            </el-button>
            <el-button type="danger" size="small" @click="handleDeleteUser(scope.row)">
              <el-icon><Delete /></el-icon>
              删除
            </el-button>
          </template>
        </el-table-column>
      </el-table>
      
      <!-- 分页 -->
      <div class="pagination">
        <el-pagination
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
          :current-page="currentPage"
          :page-sizes="[10, 20, 50, 100]"
          :page-size="pageSize"
          layout="total, sizes, prev, pager, next, jumper"
          :total="filteredUsers.length"
        ></el-pagination>
      </div>
    </el-card>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { Edit, Delete } from '@element-plus/icons-vue'

// 搜索表单
const searchForm = ref({
  username: '',
  email: '',
  status: ''
})

// 分页
const currentPage = ref(1)
const pageSize = ref(10)

// 模拟用户数据
const users = ref([
  { id: 1, username: 'admin', email: 'admin@example.com', role: 'admin', status: 'active', avatar: 'https://xsgames.co/randomusers/avatar.php?g=pixel', createdAt: '2025-01-15 10:30:00', updatedAt: '2025-12-10 14:20:00' },
  { id: 2, username: 'user1', email: 'user1@example.com', role: 'user', status: 'active', avatar: 'https://xsgames.co/randomusers/avatar.php?g=female', createdAt: '2025-02-20 15:45:00', updatedAt: '2025-12-05 09:10:00' },
  { id: 3, username: 'user2', email: 'user2@example.com', role: 'user', status: 'inactive', avatar: 'https://xsgames.co/randomusers/avatar.php?g=male', createdAt: '2025-03-10 08:20:00', updatedAt: '2025-11-20 16:30:00' },
  { id: 4, username: 'user3', email: 'user3@example.com', role: 'user', status: 'active', avatar: 'https://xsgames.co/randomusers/avatar.php?g=pixel', createdAt: '2025-04-05 11:15:00', updatedAt: '2025-12-12 11:45:00' },
  { id: 5, username: 'user4', email: 'user4@example.com', role: 'user', status: 'active', avatar: 'https://xsgames.co/randomusers/avatar.php?g=female', createdAt: '2025-05-18 13:30:00', updatedAt: '2025-12-08 10:15:00' }
])

// 筛选用户
const filteredUsers = computed(() => {
  return users.value.filter(user => {
    const matchesUsername = searchForm.value.username
      ? user.username.includes(searchForm.value.username)
      : true
    const matchesEmail = searchForm.value.email
      ? user.email.includes(searchForm.value.email)
      : true
    const matchesStatus = searchForm.value.status
      ? user.status === searchForm.value.status
      : true
    return matchesUsername && matchesEmail && matchesStatus
  })
})

// 搜索
const handleSearch = () => {
  currentPage.value = 1
}

// 重置
const handleReset = () => {
  searchForm.value = {
    username: '',
    email: '',
    status: ''
  }
  currentPage.value = 1
}

// 新增用户
const handleAddUser = () => {
  // 这里可以打开新增用户对话框
  console.log('添加用户')
}

// 编辑用户
const handleEditUser = (user) => {
  // 这里可以打开编辑用户对话框
  console.log('编辑用户:', user)
}

// 删除用户
const handleDeleteUser = (user) => {
  // 这里可以打开删除确认对话框
  console.log('删除用户:', user)
}

// 状态变更
const handleStatusChange = (user) => {
  console.log('状态变更:', user)
}

// 分页大小变更
const handleSizeChange = (size) => {
  pageSize.value = size
}

// 当前页变更
const handleCurrentChange = (current) => {
  currentPage.value = current
}
</script>

<style scoped>
.users-page {
  width: 100%;
  height: 100%;
}

.page-header {
  margin-bottom: 30px;
}

.page-title {
  font-size: 28px;
  font-weight: bold;
  margin: 0 0 8px 0;
  color: #303133;
}

.page-subtitle {
  font-size: 14px;
  color: #909399;
  margin: 0;
}

.filter-card {
  margin-bottom: 20px;
}

.filter-actions {
  display: flex;
  justify-content: flex-end;
  margin-top: 10px;
}

.users-card {
  margin-bottom: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-weight: 500;
  color: #606266;
}

.user-count {
  color: #909399;
  font-size: 14px;
}

.pagination {
  margin-top: 20px;
  display: flex;
  justify-content: flex-end;
}
</style>