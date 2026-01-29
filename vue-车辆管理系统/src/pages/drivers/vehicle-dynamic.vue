<template>
  <div class="vehicle-dynamic-container">
    <el-card shadow="hover" class="page-card">
      <template #header>
        <div class="card-header">
          <span class="header-title">车辆动态管理</span>
          <el-button type="primary" @click="addDynamic">
            <el-icon><Plus /></el-icon>
            新增车辆动态
          </el-button>
        </div>
      </template>
      
      <!-- 搜索和筛选区域 -->
      <el-form :inline="true" class="search-form" label-width="80px">
        <el-form-item label="车牌">
          <el-input v-model="searchForm.plate_number" placeholder="请输入车牌" clearable />
        </el-form-item>
        <el-form-item label="故障现象">
          <el-input v-model="searchForm.fault_phenomenon" placeholder="请输入故障现象" clearable />
        </el-form-item>
        <el-form-item label="相关人员">
          <el-input v-model="searchForm.related_personnel" placeholder="请输入相关人员" clearable />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleSearch">搜索</el-button>
          <el-button @click="resetSearch">重置</el-button>
        </el-form-item>
      </el-form>
      
      <!-- 车辆动态列表 -->
      <el-table
        :data="dynamicList"
        stripe
        border
        style="width: 100%"
        :row-key="row => row.id"
        v-loading="loading"
      >
        <el-table-column type="selection" width="55" />
        <el-table-column prop="id" label="ID" width="80" align="center" />
        <el-table-column prop="plate_number" label="车牌" min-width="120" />
        <el-table-column prop="fault_phenomenon" label="故障现象" min-width="180" />
        <el-table-column prop="start_date" label="起始日期" min-width="120" />
        <el-table-column prop="end_date" label="结束日期" min-width="120" />
        <el-table-column prop="related_personnel" label="相关人员" min-width="120" />
        <el-table-column prop="remarks" label="备注" min-width="200" show-overflow-tooltip />
        <el-table-column label="操作" width="150" align="center" fixed="right">
          <template #default="scope">
            <el-button type="primary" size="small" @click="editDynamic(scope.row)">
              <el-icon><Edit /></el-icon>
              编辑
            </el-button>
            <el-button type="danger" size="small" @click="deleteDynamic(scope.row.id)">
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
    
    <!-- 新增/编辑车辆动态对话框 -->
    <el-dialog
      v-model="dialogVisible"
      :title="isEdit ? '编辑车辆动态' : '新增车辆动态'"
      width="600px"
    >
      <el-form :model="dynamicForm" :rules="dynamicRules" ref="dynamicFormRef" label-width="100px">
        <el-form-item label="车牌" prop="plate_number">
          <el-input v-model="dynamicForm.plate_number" placeholder="请输入车牌" />
        </el-form-item>
        <el-form-item label="故障现象" prop="fault_phenomenon">
          <el-input v-model="dynamicForm.fault_phenomenon" placeholder="请输入故障现象" type="textarea" :rows="3" />
        </el-form-item>
        <el-form-item label="起始日期" prop="start_date">
          <el-date-picker
            v-model="dynamicForm.start_date"
            type="date"
            placeholder="选择起始日期"
            style="width: 100%"
          />
        </el-form-item>
        <el-form-item label="结束日期" prop="end_date">
          <el-date-picker
            v-model="dynamicForm.end_date"
            type="date"
            placeholder="选择结束日期"
            style="width: 100%"
          />
        </el-form-item>
        <el-form-item label="相关人员" prop="related_personnel">
          <el-input v-model="dynamicForm.related_personnel" placeholder="请输入相关人员" />
        </el-form-item>
        <el-form-item label="备注" prop="remarks">
          <el-input v-model="dynamicForm.remarks" placeholder="请输入备注" type="textarea" :rows="3" />
        </el-form-item>
      </el-form>
      <template #footer>
        <div class="dialog-footer">
          <el-button @click="dialogVisible = false">取消</el-button>
          <el-button type="primary" @click="saveDynamic">保存</el-button>
        </div>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { Plus, Edit, Delete } from '@element-plus/icons-vue'
import { ElMessageBox, ElMessage } from 'element-plus'
import axios from 'axios'

// 搜索表单
const searchForm = reactive({
  plate_number: '',
  fault_phenomenon: '',
  related_personnel: ''
})

// 加载状态
const loading = ref(false)

// 车辆动态列表
const dynamicList = ref([])

// 分页配置
const pagination = reactive({
  currentPage: 1,
  pageSize: 10,
  total: 3
})

// 对话框配置
const dialogVisible = ref(false)
const isEdit = ref(false)
const dynamicFormRef = ref(null)

// 车辆动态表单
const dynamicForm = reactive({
  id: '',
  plate_number: '',
  fault_phenomenon: '',
  start_date: '',
  end_date: '',
  related_personnel: '',
  remarks: ''
})

// 表单验证规则
const dynamicRules = {
  plate_number: [
    { required: true, message: '请输入车牌', trigger: 'blur' }
  ],
  fault_phenomenon: [
    { required: true, message: '请输入故障现象', trigger: 'blur' }
  ],
  start_date: [
    { required: true, message: '请选择起始日期', trigger: 'change' }
  ],
  end_date: [
    { required: true, message: '请选择结束日期', trigger: 'change' }
  ],
  related_personnel: [
    { required: true, message: '请输入相关人员', trigger: 'blur' }
  ]
}

// 搜索车辆动态
const handleSearch = async () => {
  loading.value = true
  try {
    const response = await axios.get('/vehicle_dynamic/', {
      params: {
        ...searchForm,
        page: pagination.currentPage,
        page_size: pagination.pageSize
      }
    })
    dynamicList.value = response.data || []
    pagination.total = response.length || 0
  } catch (error) {
    ElMessage.error('获取车辆动态列表失败，请稍后重试')
    console.error('获取车辆动态列表失败:', error)
  } finally {
    loading.value = false
  }
}

// 重置搜索
const resetSearch = () => {
  Object.assign(searchForm, {
    plate_number: '',
    fault_phenomenon: '',
    related_personnel: ''
  })
  handleSearch()
}

// 新增车辆动态
const addDynamic = () => {
  isEdit.value = false
  Object.assign(dynamicForm, {
    id: '',
    plate_number: '',
    fault_phenomenon: '',
    start_date: '',
    end_date: '',
    related_personnel: '',
    remarks: ''
  })
  dialogVisible.value = true
}

// 编辑车辆动态
const editDynamic = (row) => {
  isEdit.value = true
  Object.assign(dynamicForm, { ...row })
  dialogVisible.value = true
}

// 删除车辆动态
const deleteDynamic = async (id) => {
  ElMessageBox.confirm('确定要删除该车辆动态记录吗？', '删除确认', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning'
  }).then(async () => {
    loading.value = true
    try {
      await axios.delete(`/vehicle_dynamic/${id}`)
      ElMessage.success('删除成功')
      handleSearch() // 重新查询数据
    } catch (error) {
      ElMessage.error('删除失败，请稍后重试')
      console.error('删除车辆动态失败:', error)
    } finally {
      loading.value = false
    }
  }).catch(() => {
    // 取消删除
  })
}

// 保存车辆动态
const saveDynamic = async () => {
  dynamicFormRef.value.validate(async (valid) => {
    if (valid) {
      loading.value = true
      try {
        if (isEdit.value) {
          // 编辑操作
          await axios.put(`/vehicle_dynamic/${dynamicForm.id}`, dynamicForm)
          ElMessage.success('编辑成功')
        } else {
          // 新增操作
          await axios.post('/vehicle_dynamic/', dynamicForm)
          ElMessage.success('新增成功')
        }
        dialogVisible.value = false
        handleSearch() // 重新查询数据
      } catch (error) {
        ElMessage.error(isEdit.value ? '编辑失败，请稍后重试' : '新增失败，请稍后重试')
        console.error(isEdit.value ? '编辑车辆动态失败:' : '新增车辆动态失败:', error)
      } finally {
        loading.value = false
      }
    }
  })
}

// 分页变化
const handleSizeChange = (size) => {
  pagination.pageSize = size
  pagination.currentPage = 1 // 重置到第一页
  handleSearch() // 重新查询数据
}

const handleCurrentChange = (current) => {
  pagination.currentPage = current
  handleSearch() // 重新查询数据
}

// 页面加载时执行
onMounted(() => {
  handleSearch()
})
</script>

<style scoped>
.vehicle-dynamic-container {
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