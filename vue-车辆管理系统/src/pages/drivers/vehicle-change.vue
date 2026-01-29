<template>
  <div class="vehicle-change-container">
    <el-card shadow="hover" class="page-card">
      <template #header>
        <div class="card-header">
          <span class="header-title">换车记录管理</span>
          <el-button type="primary" @click="addChange">
            <el-icon><Plus /></el-icon>
            新增换车记录
          </el-button>
        </div>
      </template>
      
      <!-- 搜索和筛选区域 -->
      <el-form :inline="true" class="search-form" label-width="80px">
        <el-form-item label="司机姓名">
          <el-input v-model="searchForm.driver_name" placeholder="请输入司机姓名" clearable />
        </el-form-item>
        <el-form-item label="原车牌号">
          <el-input v-model="searchForm.original_plate" placeholder="请输入原车牌号" clearable />
        </el-form-item>
        <el-form-item label="更换后车牌号">
          <el-input v-model="searchForm.new_plate" placeholder="请输入更换后车牌号" clearable />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleSearch">搜索</el-button>
          <el-button @click="resetSearch">重置</el-button>
        </el-form-item>
      </el-form>
      
      <!-- 换车记录列表 -->
      <el-table
        :data="paginatedList"
        stripe
        border
        style="width: 100%"
        :row-key="row => row.id"
        v-loading="loading"
      >
        <el-table-column type="selection" width="55" />
        <el-table-column prop="id" label="ID" width="80" align="center" />
        <el-table-column prop="driver_name" label="司机姓名" min-width="120" />
        <el-table-column prop="change_time" label="换车时间" min-width="180" />
        <el-table-column prop="original_plate" label="原车牌" min-width="120" />
        <el-table-column prop="new_plate" label="更换后车牌" min-width="120" />
        <el-table-column label="操作" width="150" align="center" fixed="right">
          <template #default="scope">
            <el-button type="primary" size="small" @click="editChange(scope.row)">
              <el-icon><Edit /></el-icon>
              编辑
            </el-button>
            <el-button type="danger" size="small" @click="deleteChange(scope.row.id)">
              <el-icon><Delete /></el-icon>
              删除
            </el-button>
          </template>
        </el-table-column>
      </el-table>
      
      <!-- 分页 -->
      <div class="pagination-container">
        <el-pagination
          v-model:current-page="pagination.currentPage"
          v-model:page-size="pagination.pageSize"
          :page-sizes="[10, 20, 50, 100]"
          layout="total, sizes, prev, pager, next, jumper"
          :total="pagination.total"
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
        />
      </div>
    </el-card>
    
    <!-- 新增/编辑换车记录对话框 -->
    <el-dialog
      v-model="dialogVisible"
      :title="isEdit ? '编辑换车记录' : '新增换车记录'"
      width="500px"
    >
      <el-form :model="changeForm" :rules="changeRules" ref="changeFormRef" label-width="100px">
         <el-form-item label="司机id" prop="driver_id">
          <el-input v-model="changeForm.id" placeholder="请输入司机姓名" />
        </el-form-item>
        <el-form-item label="司机姓名" prop="driver_name">
          <el-input v-model="changeForm.driver_name" placeholder="请输入司机姓名" />
        </el-form-item>
        <el-form-item label="换车时间" prop="change_time">
          <el-date-picker
            v-model="changeForm.change_time"
            type="datetime"
            value-format="YYYY-MM-DD HH:mm:ss"
            placeholder="选择换车时间"
            style="width: 100%"
          />
        </el-form-item>
        <el-form-item label="原车牌" prop="original_plate">
          <el-input v-model="changeForm.original_plate" placeholder="请输入原车牌号" />
        </el-form-item>
        <el-form-item label="更换后车牌" prop="new_plate">
          <el-input v-model="changeForm.new_plate" placeholder="请输入更换后车牌号" />
        </el-form-item>
      </el-form>
      <template #footer>
        <div class="dialog-footer">
          <el-button @click="dialogVisible = false">取消</el-button>
          <el-button type="primary" @click="saveChange">保存</el-button>
        </div>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, computed } from 'vue'
import { Plus, Edit, Delete } from '@element-plus/icons-vue'
import { ElMessageBox, ElMessage } from 'element-plus'
import axios from 'axios'

// 搜索表单
const searchForm = reactive({
  driver_name: '',
  original_plate: '',
  new_plate: ''
})

// 换车记录列表
const changeList = ref([
  {
    id: 1,
    driver_name: '张三',
    change_time: '2024-02-15 10:30:00',
    original_plate: '京A12345',
    new_plate: '京B67890'
  },
  {
    id: 2,
    driver_name: '李四',
    change_time: '2024-03-20 14:20:00',
    original_plate: '京C24680',
    new_plate: '京D13579'
  },
  {
    id: 3,
    driver_name: '王五',
    change_time: '2024-04-10 09:15:00',
    original_plate: '京E98765',
    new_plate: '京F43210'
  }
])

// 分页配置
const pagination = reactive({
  currentPage: 1,
  pageSize: 10,
  total: 0
})

// 加载状态
const loading = ref(false)

// 对话框配置
const dialogVisible = ref(false)
const isEdit = ref(false)
const changeFormRef = ref(null)

// 换车记录表单
const changeForm = reactive({
  id: '',
  driver_name: '',
  change_time: '',
  original_plate: '',
  new_plate: ''
})

// 表单验证规则
const changeRules = {
  driver_name: [
    { required: true, message: '请输入司机姓名', trigger: 'blur' }
  ],
  change_time: [
    { required: true, message: '请选择换车时间', trigger: 'change' }
  ],
  original_plate: [
    { required: true, message: '请输入原车牌号', trigger: 'blur' }
  ],
  new_plate: [
    { required: true, message: '请输入更换后车牌号', trigger: 'blur' }
  ]
}

// 分页后的数据列表
const paginatedList = computed(() => {
  const start = (pagination.currentPage - 1) * pagination.pageSize
  const end = start + pagination.pageSize
  return changeList.value.slice(start, end)
})

// 搜索换车记录
const handleSearch = async () => {
  loading.value = true
  try {
    const params = {
      ...searchForm
    }
    const response = await axios.get('/vehicle_change/', { params })
    changeList.value = response.data
    pagination.total = response.data.length
  } catch (error) {
    console.error('获取换车记录失败:', error)
    ElMessage.error('获取换车记录失败，请稍后重试')
  } finally {
    loading.value = false
  }
}

// 重置搜索
const resetSearch = () => {
  Object.assign(searchForm, {
    driver_name: '',
    original_plate: '',
    new_plate: ''
  })
  handleSearch()
}

// 新增换车记录
const addChange = () => {
  isEdit.value = false
  Object.assign(changeForm, {
    id: '',
    driver_name: '',
    change_time: '',
    original_plate: '',
    new_plate: ''
  })
  dialogVisible.value = true
}

// 编辑换车记录
const editChange = (row) => {
  isEdit.value = true
  Object.assign(changeForm, { ...row })
  dialogVisible.value = true
}

// 删除换车记录
const deleteChange = async (id) => {
  ElMessageBox.confirm('确定要删除该换车记录吗？', '删除确认', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning'
  }).then(async () => {
    loading.value = true
    try {
      await axios.delete(`/vehicle_change/delete/${id}`)
      ElMessage.success('删除成功')
      handleSearch()
    } catch (error) {
      console.error('删除失败:', error)
      ElMessage.error('删除失败，请稍后重试')
    } finally {
      loading.value = false
    }
  }).catch(() => {
    // 取消删除
  })
}

// 保存换车记录
const saveChange = async () => {
  changeFormRef.value.validate(async (valid) => {
    if (valid) {
      loading.value = true
      try {
        if (isEdit.value) {
          await axios.put(`/vehicle_change/edit/${changeForm.id}`, changeForm)
          ElMessage.success('编辑成功')
        } else {
          await axios.post('/vehicle_change/add', changeForm)
          ElMessage.success('新增成功')
        }
        dialogVisible.value = false
        handleSearch()
      } catch (error) {
        console.error('保存失败:', error)
        ElMessage.error(isEdit.value ? '编辑失败，请稍后重试' : '新增失败，请稍后重试')
      } finally {
        loading.value = false
      }
    }
  })
}

// 分页变化
const handleSizeChange = (size) => {
  pagination.pageSize = size
  pagination.currentPage = 1
  handleSearch()
}

const handleCurrentChange = (current) => {
  pagination.currentPage = current
  handleSearch()
}

// 页面加载时执行
onMounted(() => {
  handleSearch()
})
</script>

<style scoped>
.vehicle-change-container {
  padding: 20px;
  background-color: #f5f7fa;
  min-height: calc(100vh - 60px);
}

.page-card {
  margin-bottom: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.header-title {
  font-size: 18px;
  font-weight: 600;
  color: #303133;
}

.search-form {
  margin-bottom: 20px;
  padding: 15px;
  background-color: #f0f2f5;
  border-radius: 4px;
}

.pagination-container {
  margin-top: 20px;
  text-align: right;
}

.dialog-footer {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
}
</style>