<template>
  <div style="padding: 20px;">
    <h2 > 角色管理</h2>
  <!--添加权限-->
    <el-row :gutter="10"  class = 'create'>
         <el-col :span="12">
            <el-input v-model="input" style="width: 240px" placeholder="Please input" />
           <el-button type="success" @click="loadroles">搜索</el-button>
         </el-col>
      <el-col :span="3">
        <el-button type="primary" @click="openDialog('add')">新增角色</el-button>
      </el-col>
      <el-col :span="2">
        <el-button type="success" @click="loadroles">刷新</el-button>
      </el-col>
    </el-row>

    <!-- 加载状态 -->
    <el-loading v-if="loading" text="加载中..." />

    <!-- 权限列表 -->
    <el-table :data="roles" border style="width: 100%" v-else>
      <el-table-column prop="role_name" label="角色名称" />
      <el-table-column prop="role_description" label="描述" />
      <el-table-column label="权限">
         <el-button type="default" @click="getPermissions()">权限</el-button>
      </el-table-column>

        <el-table-column label="操作" width="180">
        <template #default="{ row }">
          <el-button size="small" type="warning" @click="openDialog('edit', row)">编辑</el-button>
          <el-button size="small" type="danger" @click="handleDelete(row)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>

    <el-dialog
      v-model="dialogVisible"
      :title="dialogTitle"
      width="500px"
      @close="resetForm"
    >
      <el-form :model="form" :rules="rules" ref="formRef" label-width="80px">
        <el-form-item label="角色名称" prop="role_name">
          <el-input v-model="form.role_name" placeholder="请输入角色名称" :disabled="isEditMode"/>
        </el-form-item>
        <el-form-item label="描述" prop="role_description">
          <el-input v-model="form.role_description" type="textarea" placeholder="请输入描述" />
        </el-form-item>
      </el-form>

      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="handleSubmit" :loading="submitting">
          确定
        </el-button>
      </template>
    </el-dialog>

     <el-dialog
      v-model="permissionDialogVisible"
      :title="`角色权限 - ${currentRoleName}`"
      width="600px"
    >
      <el-transfer
        v-model="selectedPermissions"
        :data="allPermissions"
        :titles="['所有权限', '已选权限']"
        :button-texts="['移除', '添加']"
         :format="{
          noChecked: '${total}',
          hasChecked: '${checked}/${total}'
        }"
        filterable
        filter-placeholder="搜索权限"
      />

      <template #footer>
        <el-button @click="permissionDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="saveRolePermissions" :loading="savingPermission">
          保存
        </el-button>
      </template>
    </el-dialog>




  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import role from "~/pages/role/role.js";

// 数据
const roles = ref([])
const formRef= ref(null)
const form = ref({
  id: null,
  role_name: '',
  role_description: ''
})
const dialogTitle = ref()

//状态
const loading = ref(false)
const dialogVisible = ref(false)
const isEditMode = ref(false)
const submitting = ref(false)


// 获取角色列表
const getroles = async () => {
  loading.value = true
  try {
    // 请求后端接口（替换为你的地址）
    const res = await role.getAll()

    // 后端返回格式：{ "data": [ { "id": 1, "name": "admin", "description": "管理员权限" }, ... ] }
    roles.value = res.data.data  // ✅ 直接取 data 字段

  } catch (error) {
    alert('获取权限失败：' + error.message)
  } finally {
    loading.value = false
  }
}

// 获取权限列表
const getpermissions = async () => {
  loading.value = true
  try {
    // 获取权限列表
    const res = await role.getPermissions()

    // 后端返回格式：{ "data": [ { "id": 1, "name": "admin", "description": "管理员权限" }, ... ] }
    permissions.value = res.data.data  // ✅ 直接取 data 字段

  } catch (error) {
    alert('获取权限失败：' + error.message)
  } finally {
    loading.value = false
  }
}

//编辑权限
const openDialog = (type, row) => {
  dialogVisible.value = true
  if (type === 'add'){
    dialogTitle.value = '新增角色'
    isEditMode.value = false
    form.value = {
      role_name: '',
      role_description: ''
    }
  }
  else if (type === 'edit'){
    dialogTitle.value = '编辑角色'
    isEditMode.value = true
    form.value = {
      role_name: row.role_name,
      role_description: row.role_description
    }
  }
}
const handleSubmit =async () => {
  let res
  formRef.value.validate(async (valid) => {
    if (valid) {
      submitting.value = true
      console.log(isEditMode)
        if(isEditMode.value)

          res = await role.update(form.value)
        else {
          console.log('create')
          res = await role.create(form.value)
        }
      submitting.value = false
      dialogVisible.value = false
      await getroles()
    }
  })
}

// 删除权限
const handleDelete = async (row) => {
  console.log(row.role_name)
  await role.delete(row.role_name).then(() => {
    getroles()
  }).catch((error) => {
    alert('删除权限失败：' + error.message)
  })

}

// 页面加载时自动获取数据
onMounted(() => {
  getroles()
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