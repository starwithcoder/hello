<template>
  <div style="padding: 20px;">
    <h2 > 权限管理</h2>
  <!--上方导航-->
       <el-row :gutter="10"  class = 'create'>
         <el-col :span="12">
            <el-input v-model="search" style="width: 240px" placeholder="Please input" />
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

    <!-- 权限对话框 -->
     <el-dialog
      v-model="dialogVisible"
      :title="dialogTitle"
      width="500px"
      @close="resetForm"
    >
      <el-form :model="form" :rules="rules" ref="formRef" label-width="80px">
        <el-form-item label="权限名称" prop="name">
          <el-input v-model="form.name" placeholder="请输入权限名称" />
        </el-form-item>
        <el-form-item label="描述" prop="description">
          <el-input v-model="form.description" type="textarea" placeholder="请输入描述" />
        </el-form-item>
      </el-form>

      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="handleSubmit" :loading="submitting">
          确定
        </el-button>
      </template>
    </el-dialog>

  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import permission from "~/pages/permission/permission.js";

// 数据
const permissions = ref([])
const search = ref('')

//状态
const dialogVisible = ref(false)
const loading = ref(false)
const dialogTitle = ref('')
const formRef = ref(null)
const submitting = ref(false)

// 表单数据
const form = ref({
  id: null,
  name: '',
  description: ''
})

// 表单验证规则
const rules = {
  name: [
    { required: true, message: '请输入权限名称', trigger: 'blur' },
    { min: 2, max: 20, message: '长度在 2 到 20 个字符', trigger: 'blur' }
  ],
  description: [
    { required: true, message: '请输入描述', trigger: 'blur' }
  ]
}

// 获取全部权限列表
const loadPermissions = async () => {
  loading.value = true
  try {
    const keyword = search.value.trim()
    let res
    if (keyword) {
       res = await permission.search(keyword)
      console.log(keyword)

    }else{
       res = await permission.getAll()
    }

    // 后端返回格式：{ "data": [ { "id": 1, "name": "admin", "description": "管理员权限" }, ... ] }
    permissions.value = res.data.data  // ✅ 直接取 data 字段

  } catch (error) {
    alert('获取权限失败：' + error.message)
  } finally {
    loading.value = false
  }
}



//编辑权限
const openDialog = (type,row) => {
if (type === 'add') {
  dialogVisible.value = true
  dialogTitle.value = '新增权限'
  form.value = {
    id: null,
    permission_name: '',
    description: ''
  }
} else if (type === 'edit') {
  dialogVisible.value = true
  dialogTitle.value = '编辑权限'
  form.value = {
    id: row.id,
    name: row.name,
    description: row.description
  }
}
}
const handleSubmit =async () => {
  let res

  formRef.value.validate(async (valid) => {

    if (valid) {
      submitting.value = true
      try {
         if(form.value.id)
      {
        res = await permission.update(form.value)
        console.log('update')
      }
      else {
        console.log('create')
        res = await permission.create(form.value)

      }
      }
      catch (error) {
        alert('保存权限失败：' + error.message)
      }

      submitting.value = false
      dialogVisible.value = false
      await loadPermissions()
    }
  })


}



// 删除权限
const handleDelete = async (permission_id) => {
  console.log(permission_id)
  await permission.delete(permission_id).then(() => {
    loadPermissions()
  }).catch((error) => {
    alert('删除权限失败：' + error.message)
  })
}

// 页面加载时自动获取数据
onMounted(() => {
  loadPermissions()
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