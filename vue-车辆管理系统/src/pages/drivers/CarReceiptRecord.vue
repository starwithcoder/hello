<template>
  <div class="vehicle-recall-container">
    <el-card shadow="hover" class="page-card">
      <template #header>
        <div class="card-header">
          <span class="header-title">收车记录管理</span>
          <el-button type="primary" @click="addRecall">
            <el-icon><Plus /></el-icon>
            新增收车记录
          </el-button>
        </div>
      </template>
      
      <!-- 搜索和筛选区域 -->
      <el-form :inline="true" class="search-form" label-width="80px">
        <el-form-item label="姓名">
          <el-input v-model="searchForm.name" placeholder="请输入姓名" clearable />
        </el-form-item>
        <el-form-item label="车牌">
          <el-input v-model="searchForm.plate_number" placeholder="请输入车牌" clearable />
        </el-form-item>
        <el-form-item label="日期">
          <el-date-picker
            v-model="searchForm.receipt_date"
            value-format="YYYY-MM-DD HH:mm:ss"
            type="date"
            placeholder="选择日期"
            style="width: 180px"
          />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleSearch">搜索</el-button>
          <el-button @click="resetSearch">重置</el-button>
        </el-form-item>
      </el-form>
      
      <!-- 收车记录列表 -->
      <el-table
        :data="recallList"
        stripe
        border
        style="width: 100%"
        :row-key="row => row.id"
        v-loading="loading"
      >
        <el-table-column type="selection" width="55" />
        <el-table-column prop="id" label="司机ID" width="80" align="center" />
        <el-table-column prop="name" label="司机姓名" min-width="120" />
        <el-table-column prop="plate_number" label="回收车牌" min-width="120" />
        <el-table-column prop="receipt_date" label="回收日期" min-width="120" />

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
    
    <!-- 新增/编辑收车记录对话框 -->
    <el-dialog
      v-model="dialogVisible"
      :title="isEdit ? '编辑收车记录' : '新增收车记录'"
      width="400px"
    >
      <el-form :model="recallForm" :rules="recallRules" ref="recallFormRef" label-width="100px">
        <el-form-item label="id" prop="id">
          <el-input v-model="recallForm.id" placeholder="请输入id" />
        </el-form-item>
        <el-form-item label="姓名" prop="name">
          <el-input v-model="recallForm.name" placeholder="请输入姓名" />
        </el-form-item>
        <el-form-item label="车牌" prop="plate_number">
          <el-input v-model="recallForm.plate_number" placeholder="请输入车牌" />
        </el-form-item>
        <el-form-item label="日期" prop="receipt_date">
          <el-date-picker
            v-model="recallForm.receipt_date"
            type="date"
            value-format="YYYY-MM-DD HH:mm:ss"
            placeholder="选择日期"
            style="width: 100%"
          />
        </el-form-item>
      </el-form>
      <template #footer>
        <div class="dialog-footer">
          <el-button @click="dialogVisible = false">取消</el-button>
          <el-button type="primary" @click="saveRecall">保存</el-button>
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
  name: '',
  plate_number: '',
  receipt_date: ''
})

// 加载状态
const loading = ref(false)

// 收车记录列表
const recallList = ref([])

// 分页配置
const pagination = reactive({
  currentPage: 1,
  pageSize: 10,
  total: 3
})

// 对话框配置
const dialogVisible = ref(false)
const isEdit = ref(false)
const recallFormRef = ref(null)

// 收车记录表单
const recallForm = reactive({
  id: '',
  name: '',
  plate_number: '',
  receipt_date: ''
})

// 表单验证规则
const recallRules = {
  name: [
    { required: true, message: '请输入姓名', trigger: 'blur' }
  ],
  plate_number: [
    { required: true, message: '请输入车牌', trigger: 'blur' }
  ],
  receipt_date: [
    { required: true, message: '请选择日期', trigger: 'change' }
  ]
}

// 搜索收车记录
const handleSearch = async () => {
  loading.value = true
  try {
    // 处理搜索条件中的日期格式
    const searchParams = {
      ...searchForm,
      page: pagination.currentPage,

    }
    
    const response = await axios.get('/carReceiptRecord/', {
      params: searchParams
    })
    console.log('response')
    console.log(response.data)
    // 正确解析响应数据，通常API响应格式为{ data: [...], total: 100 }
    recallList.value = response.data.data || response.data || []
    pagination.total = response.data.total || 0
  } catch (error) {
    ElMessage.error('获取收车记录列表失败，请稍后重试')
    console.error('获取收车记录列表失败:', error)
  } finally {
    loading.value = false
  }
}

// 重置搜索
const resetSearch = () => {
  Object.assign(searchForm, {
    name: '',
    plate_number: '',
    receipt_date: ''
  })
  handleSearch()
}

// 新增收车记录
const addRecall = () => {
  isEdit.value = false
  Object.assign(recallForm, {
    id: '',
    name: '',
    plate_number: '',
    receipt_date: ''
  })
  dialogVisible.value = true
}

// 编辑收车记录
const editRecall = (row) => {
  isEdit.value = true
  Object.assign(recallForm, { ...row })
  dialogVisible.value = true
}

// 删除收车记录
const deleteRecall = async (id) => {
  ElMessageBox.confirm('确定要删除该收车记录吗？', '删除确认', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning'
  }).then(async () => {
    loading.value = true
    try {
      await axios.delete(`/carReceiptRecord/${id}`)
      ElMessage.success('删除成功')
      // 删除成功后刷新列表
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

// 保存收车记录
const saveRecall = async () => {
  recallFormRef.value.validate(async (valid) => {
    if (valid) {
      loading.value = true
      try {
        // 处理日期格式，确保发送字符串给后端
        const formData = {
          ...recallForm,
        }
        
        if (isEdit.value) {
          // 编辑操作
          await axios.put(`/carReceiptRecord/${formData.id}`, formData)
        } else {
          // 新增操作
          await axios.post('/carReceiptRecord/', formData)
        }
        dialogVisible.value = false
        ElMessage.success(isEdit.value ? '编辑成功' : '新增成功')
        // 保存成功后刷新列表
        handleSearch()
      } catch (error) {
        console.error('保存失败:', error)
        ElMessage.error('保存失败，请稍后重试')
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
.vehicle-recall-container {
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