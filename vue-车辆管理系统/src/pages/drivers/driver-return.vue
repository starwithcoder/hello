<template>
  <div class="driver-return-container">
    <el-card shadow="hover" class="page-card">
      <template #header>
        <div class="card-header">
          <span class="header-title">司机退车管理</span>
          <el-button type="primary" @click="addReturn">
            <el-icon><Plus /></el-icon>
            新增退车记录
          </el-button>
        </div>
      </template>
      
      <!-- 搜索和筛选区域 -->
      <el-form :inline="true" class="search-form" label-width="80px">
        <el-form-item label="司机姓名">
          <el-input v-model="searchForm.driver_name" placeholder="请输入司机姓名" clearable />
        </el-form-item>
        <el-form-item label="车牌号">
          <el-input v-model="searchForm.plate_number" placeholder="请输入车牌号" clearable />
        </el-form-item>
        <el-form-item label="平台">
          <el-select v-model="searchForm.platform" placeholder="请选择平台" clearable>
            <el-option label="平台A" value="platformA" />
            <el-option label="平台B" value="platformB" />
            <el-option label="平台C" value="platformC" />
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleSearch">搜索</el-button>
          <el-button @click="resetSearch">重置</el-button>
        </el-form-item>
      </el-form>
      
      <!-- 退车记录列表 -->
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
        <el-table-column prop="platform" label="平台" min-width="100">
          <template #default="scope">
            <el-tag type="info">{{ scope.row.platform === 'platformA' ? '平台A' : scope.row.platform === 'platformB' ? '平台B' : '平台C' }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="plate_number" label="车牌号" min-width="120" />
        <el-table-column prop="driver_phone" label="司机手机号" min-width="150" />
        <el-table-column prop="registration_date" label="注册日期" min-width="150" />
        <el-table-column prop="return_date" label="退车日期" min-width="150" />
        <el-table-column prop="is_over_30_days" label="是否满30天" width="120" align="center">
          <template #default="scope">
            <el-tag :type="scope.row.is_over_30_days ? 'success' : 'danger'">
              {{ scope.row.is_over_30_days ? '是' : '否' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="is_over_60_days" label="是否满60天" width="120" align="center">
          <template #default="scope">
            <el-tag :type="scope.row.is_over_60_days ? 'success' : 'danger'">
              {{ scope.row.is_over_60_days ? '是' : '否' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="is_over_90_days" label="是否满90天" width="120" align="center">
          <template #default="scope">
            <el-tag :type="scope.row.is_over_90_days ? 'success' : 'danger'">
              {{ scope.row.is_over_90_days ? '是' : '否' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="remarks" label="备注" min-width="200" show-overflow-tooltip />
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
    
    <!-- 新增/编辑退车记录对话框 -->
    <el-dialog
      v-model="dialogVisible"
      :title="isEdit ? '编辑退车记录' : '新增退车记录'"
      width="500px"
    >
      <el-form :model="returnForm" :rules="returnRules" ref="returnFormRef" label-width="100px">
        <el-form-item label="司机ID" prop="id">
          <el-input v-model="returnForm.id" placeholder="请输入司机id" />
        </el-form-item>
        <el-form-item label="司机姓名" prop="driver_name">
          <el-input v-model="returnForm.driver_name" placeholder="请输入司机姓名" />
        </el-form-item>

        <el-form-item label="车牌号" prop="plate_number">
          <el-input v-model="returnForm.plate_number" placeholder="请输入车牌号" />
        </el-form-item>

        <el-form-item label="退车日期" prop="return_date">
          <el-date-picker
            v-model="returnForm.return_date"
            type="date"
            value-format="YYYY-MM-DD HH:mm:ss"
            placeholder="选择退车日期"
            style="width: 100%"
          />
        </el-form-item>

        <el-form-item label="备注" prop="remarks">
          <el-input
            v-model="returnForm.remarks"
            type="textarea"
            :rows="2"
            placeholder="请输入备注"
          />
        </el-form-item>
      </el-form>
      <template #footer>
        <div class="dialog-footer">
          <el-button @click="dialogVisible = false">取消</el-button>
          <el-button type="primary" @click="saveReturn">保存</el-button>
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
  plate_number: '',
  platform: ''
})

// 退车记录列表
const returnList = ref([])
const loading = ref(false)

// 分页配置
const pagination = reactive({
  currentPage: 1,
  pageSize: 10,
  total: 0
})

// 对话框配置
const dialogVisible = ref(false)
const isEdit = ref(false)
const returnFormRef = ref(null)

// 退车记录表单
const returnForm = reactive({
  id: '',
  driver_name: '',
  platform: '',
  plate_number: '',
  driver_phone: '',
  registration_date: '',
  return_date: '',
  is_over_30_days: false,
  is_over_60_days: false,
  is_over_90_days: false,
  remarks: ''
})

// 表单验证规则
const returnRules = {
  driver_name: [
    { required: true, message: '请输入司机姓名', trigger: 'blur' },
    { min: 2, max: 20, message: '长度在 2 到 20 个字符', trigger: 'blur' }
  ],
  platform: [
    { required: true, message: '请选择平台', trigger: 'change' }
  ],
  plate_number: [
    { required: true, message: '请输入车牌号', trigger: 'blur' }
  ],
  driver_phone: [
    { required: true, message: '请输入司机手机号', trigger: 'blur' },
    { pattern: /^1[3-9]\d{9}$/, message: '请输入正确的手机号码', trigger: 'blur' }
  ],
  registration_date: [
    { required: true, message: '请选择注册日期', trigger: 'change' }
  ],
  return_date: [
    { required: true, message: '请选择退车日期', trigger: 'change' }
  ]
}

// 分页列表
const paginatedList = computed(() => {
  const start = (pagination.currentPage - 1) * pagination.pageSize
  const end = start + pagination.pageSize
  return returnList.value.slice(start, end)
})

// 搜索退车记录
const handleSearch = async () => {
  loading.value = true
  try {
    const response = await axios.get('/driver_return/search', {
      params: {
        ...searchForm,
        page: pagination.currentPage,
        page_size: pagination.pageSize
      }
    })
    returnList.value = response.data
    pagination.total = response.data.length
  } catch (error) {
    console.error('获取退车记录失败:', error)
    ElMessage.error('获取退车记录失败，请稍后重试')
    returnList.value = []
    pagination.total = 0
  } finally {
    loading.value = false
  }
}

// 重置搜索
const resetSearch = () => {
  Object.assign(searchForm, {
    driver_name: '',
    plate_number: '',
    platform: ''
  })
  handleSearch()
}

// 新增退车记录
const addReturn = () => {
  isEdit.value = false
  Object.assign(returnForm, {
    id: '',
    driver_name: '',
    platform: '',
    plate_number: '',
    driver_phone: '',
    registration_date: '',
    return_date: '',
    is_over_30_days: false,
    is_over_60_days: false,
    is_over_90_days: false,
    remarks: ''
  })
  dialogVisible.value = true
}

// 编辑退车记录
const editReturn = (row) => {
  isEdit.value = true
  Object.assign(returnForm, { ...row })
  dialogVisible.value = true
}

// 删除退车记录
const deleteReturn = async (id) => {
  try {
    await ElMessageBox.confirm('确定要删除该退车记录吗？', '删除确认', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })
    
    await axios.delete(`/driver_return/${id}`)
    ElMessage.success('删除成功')
    handleSearch()
  } catch (error) {
    if (error === 'cancel') {
      return
    }
    console.error('删除退车记录失败:', error)
    ElMessage.error('删除失败，请稍后重试')
  }
}

// 保存退车记录
const saveReturn = async () => {
  returnFormRef.value.validate(async (valid) => {
    if (valid) {
      try {
        if (isEdit.value) {
          // 更新记录
          await axios.put(`/driver_return/${returnForm.id}`, returnForm)
          ElMessage.success('编辑成功')
        } else {
          // 新增记录
          await axios.post('/driver_return/add', returnForm)
          ElMessage.success('新增成功')
        }
        dialogVisible.value = false
        handleSearch()
      } catch (error) {
        console.error('保存退车记录失败:', error)
        ElMessage.error(isEdit.value ? '编辑失败，请稍后重试' : '新增失败，请稍后重试')
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
.driver-return-container {
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