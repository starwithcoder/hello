<template>
  <div style="padding: 20px;">
    <h2 > 权限管理</h2>
  <!--添加权限-->
       <el-row :gutter="10"  class = 'create'>
         <el-col :span="12">
            <el-input v-model="input" style="width: 240px" placeholder="Please input" />
           <el-button type="success" @click="loadPermissions">搜索</el-button>
         </el-col>
      <el-col :span="3">
        <el-button type="primary" @click="openDialog('add')">新增权限</el-button>
      </el-col>
      <el-col :span="2">
        <el-button type="success" @click="loadPermissions">刷新</el-button>
      </el-col>
    </el-row>



    <!-- 加载状态 -->
    <el-loading v-if="loading" text="加载中..." />

    <!-- 权限列表 -->
    <el-table :data="permissions" border style="width: 100%" v-else>
      <el-table-column prop="id" label="ID" width="80" />
      <el-table-column prop="name" label="权限名称" />
      <el-table-column prop="description" label="描述" />
        <el-table-column label="操作" width="180">
        <template #default="{ row }">
          <el-button size="small" type="warning" @click="openDialog('edit', row)">编辑</el-button>
          <el-button size="small" type="danger" @click="handleDelete(row.id)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import permission from "~/pages/permission/permission.js";

// 数据
const permissions = ref([])
const loading = ref(false)

// 获取权限列表
const getPermissions = async () => {
  loading.value = true
  try {
    // 请求后端接口（替换为你的地址）
    const res = await permission.getAll()

    // 后端返回格式：{ "data": [ { "id": 1, "name": "admin", "description": "管理员权限" }, ... ] }
    permissions.value = res.data.data  // ✅ 直接取 data 字段

  } catch (error) {
    alert('获取权限失败：' + error.message)
  } finally {
    loading.value = false
  }
}

//编辑权限
const openDialog = (id) => {

}

// 删除权限
const handleDelete = (id) => {
  console.log(id)
}

// 页面加载时自动获取数据
onMounted(() => {
  getPermissions()
})
</script>

<style scoped>
.create {
  margin-bottom: 20px;
  margin-top: 20px;
  display: flex;
  align-items: center;
  justify-content: flex-end;
}
</style>