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
      <el-table-column  label="权限">
        <template #default="{ row }">
        <el-button type="default" @click="getPermissions(row)">权限</el-button>
        </template>
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

   <el-dialog v-model="permissionDialogVisible" title="分配权限">
    <!-- 穿梭框组件 -->
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

    <!-- 对话框底部按钮 -->
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
//角色映射
const form = ref({
  id: null,
  role_name: '',
  role_description: '',
  permission_ids: []
})

const dialogTitle = ref()

const selectedPermissions = ref([

])

const allPermissions = ref([
  { key: 1, label: '查看用户', disabled: false },
  { key: 2, label: '添加用户', disabled: false },
  { key: 3, label: '删除用户', disabled: false },
  { key: 4, label: '查看角色', disabled: false },
  { key: 5, label: '分配角色', disabled: false },
])

//状态
const loading = ref(false)
const dialogVisible = ref(false)
const isEditMode = ref(false)
const submitting = ref(false)
const permissionDialogVisible = ref(false)
const savingPermission = ref(false)

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
//编辑角色
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
//增加更新角色
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
// 删除角色
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




// 获取权限列表
const getPermissions = async (row) => {
  loading.value = true
  permissionDialogVisible.value = true

  let current_permissions = row.role_permissions
  let res
  selectedPermissions.value = current_permissions.map(permission => permission.permission_id)
  form.value.role_name = row.role_name
  try {
      console.log(current_permissions)
      res = await role.getAllP()
      allPermissions.value = res.data.data.map(permission => ({
        key: permission.id,
        label: permission.name
      }))
  } catch (error) {
    alert('获取权限失败：' + error.message)
  } finally {
    loading.value = false
  }
}

// 分配权限


// 保存权限
const saveRolePermissions = () => {
  let res
  savingPermission.value = true

  // 这里可以调用后端接口，将 selectedPermissions.value 发送给服务器
  form.value.permission_ids = selectedPermissions.value
  try {
    console.log(form.value)
    res = role.update(form.value)
  }
  catch( error){
         alert('保存权限失败：' + error.message)
  }
  //关闭页面
  savingPermission.value = false
  permissionDialogVisible.value = false

}




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