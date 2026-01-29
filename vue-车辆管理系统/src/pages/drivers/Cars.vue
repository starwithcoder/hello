<template>
  <div class="vehicle-archive-container">
    <el-card shadow="hover" class="page-card">
      <template #header>
        <div class="card-header">
          <span class="header-title">汽车在库档案管理</span>
          <el-button type="primary" @click="addArchive">
            <el-icon><Plus /></el-icon>
            新增在库档案
          </el-button>
        </div>
      </template>
      
      <!-- 搜索和筛选区域 -->
      <el-form :inline="true" class="search-form" label-width="80px">
        <el-form-item label="车牌号">
          <el-input v-model="searchForm.plate_number" placeholder="请输入车牌号" clearable />
        </el-form-item>
        <el-form-item label="品牌方">
          <el-input v-model="searchForm.brand" placeholder="请输入品牌方" clearable />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleSearch" >搜索</el-button>
          <el-button @click="resetSearch" >重置</el-button>
        </el-form-item>
      </el-form>
      
      <!-- 在库档案列表 -->
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
        <el-table-column prop="plate_number" label="车牌号" min-width="120" />
        <el-table-column prop="brand" label="品牌方" min-width="100">
          <template #default="scope">
            <el-tag type="info">
              {{ getBrandText(scope.row.brand) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="vehicle_model" label="车型" min-width="150" />
        <el-table-column prop="is_annual_inspected" label="是否年审" width="120" align="center">
          <template #default="scope">
            <el-tag :type="scope.row.is_annual_inspected ? 'success' : 'danger'">
              {{ scope.row.is_annual_inspected ? '是' : '否' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="pickup_time" label="提车时间" min-width="150" />
        <el-table-column prop="is_in_use,driver_name" label="是否在用" width="120" align="center">
          <template #default="scope">
            <el-tag :type="scope.row.is_in_use ? 'success' : 'warning'">
              {{ scope.row.is_in_use ? '在用' : '停用' }}
            </el-tag>

              <!-- 显示司机姓名（如果在用） -->
            <div v-if="scope.row.is_in_use && scope.row.driver_name" style="margin-top: 4px; font-size: 12px; color: #666;">
              司机：{{ scope.row.driver_name }}
            </div>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="150" align="center" fixed="right">
          <template #default="scope">
            <el-button type="primary" size="small" @click="editArchive(scope.row)">
              <el-icon><Edit /></el-icon>
              编辑
            </el-button>
            <el-button type="danger" size="small" @click="deleteArchive(scope.row.id)">
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

          layout=" prev, pager, next, jumper"
          :total="pagination.total"
          @current-change="handleCurrentChange"
        />
      </div>
    </el-card>
    
    <!-- 新增/编辑在库档案对话框 -->
    <el-dialog
      v-model="dialogVisible"
      :title="isEdit ? '编辑在库档案' : '新增在库档案'"
      width="500px"
    >
      <el-form :model="archiveForm" :rules="archiveRules" ref="archiveFormRef" label-width="100px">
        <el-form-item label="车牌号" prop="plate_number">
          <el-input v-model="archiveForm.plate_number" placeholder="请输入车牌号" />
        </el-form-item>
        <el-form-item label="品牌方" prop="brand">
          <el-input v-model="archiveForm.brand" placeholder="请选择品牌方"/>
        </el-form-item>
        <el-form-item label="车型" prop="vehicle_model">
          <el-input v-model="archiveForm.vehicle_model" placeholder="请输入车型" />
        </el-form-item>
        <el-form-item label="是否年审" prop="is_annual_inspected">
          <el-switch v-model="archiveForm.is_annual_inspected" />
        </el-form-item>
        <el-form-item label="提车时间" prop="pickup_time">
          <el-date-picker
            v-model="archiveForm.pickup_time"
            type="date"
            value-format="YYYY-MM-DD HH:mm:ss"
            placeholder="选择提车时间"
            style="width: 100%"
          />
        </el-form-item>
      </el-form>
      <template #footer>
        <div class="dialog-footer">
          <el-button @click="dialogVisible = false">取消</el-button>
          <el-button type="primary" @click="saveArchive">保存</el-button>
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
  plate_number: '',
  brand: '',


})

// 在库档案列表 (存储所有数据)
const archiveList = ref([])

// 分页配置
const pagination = reactive({
  currentPage: 1,
  pageSize: 10,
  total: 0
})

// 分页后的数据列表
const paginatedList = computed(() => {
  const start = (pagination.currentPage - 1) * pagination.pageSize
  const end = start + pagination.pageSize
  return archiveList.value.slice(start, end)
})

// 对话框配置
const dialogVisible = ref(false)
const isEdit = ref(false)
const archiveFormRef = ref(null)

// 加载状态
const loading = ref(false)

// 在库档案表单
const archiveForm = reactive({
  id: '',
  plate_number: '',
  brand: '',
  vehicle_model: '',
  is_annual_inspected: false,
  pickup_time: '',
  is_in_use: true
})

// 表单验证规则
const archiveRules = {
  plate_number: [
    { required: true, message: '请输入车牌号', trigger: 'blur' },
    { pattern: /^[京津沪渝冀豫云辽黑湘皖鲁新苏浙赣鄂桂甘晋蒙陕吉闽贵粤青藏川宁琼使领A-Z]{1}[A-Z]{1}[A-Z0-9]{4}[A-Z0-9挂学警港澳]{1}$/, message: '请输入正确的车牌号', trigger: 'blur' }
  ],
  brand: [
    { required: true, message: '请选择品牌方', trigger: 'change' }
  ],
  vehicle_model: [
    { required: true, message: '请输入车型', trigger: 'blur' }
  ],
  pickup_time: [
    { required: true, message: '请选择提车时间', trigger: 'change' }
  ]
}

// 获取品牌方文本
const getBrandText = (brand) => {
  const brandMap = {
    volkswagen: '大众',
    toyota: '丰田',
    honda: '本田',
    buick: '别克',
    bmw: '宝马'
  }
  return brandMap[brand] || brand
}

// 搜索在库档案
const handleSearch = async () => {
  loading.value = true
  try {
    const params = {
      ...searchForm,
      page: pagination.currentPage,
    }
   const url = searchForm.plate_number || searchForm.brand || searchForm.is_in_use ? '/cars/search' : '/cars/'
    console.log(url)
    const response = await axios.get(url, { params })

    console.log(response.data)
    archiveList.value = response.data.data
    pagination.total = response.data.length
  } catch (error) {
    console.error('获取车辆列表失败:', error)
    ElMessage.error('获取车辆列表失败，请稍后重试')
  } finally {
    loading.value = false
  }
}

// 重置搜索
const resetSearch = () => {
  Object.assign(searchForm, {
    plate_number: '',
    brand: '',
    is_in_use: ''
  })
  handleSearch()
}

// 新增在库档案
const addArchive = () => {
  isEdit.value = false
  Object.assign(archiveForm, {
    id: '',
    plate_number: '',
    brand: '',
    vehicle_model: '',
    is_annual_inspected: false,
    pickup_time: '',
    is_in_use: true
  })
  dialogVisible.value = true
}

// 编辑在库档案
const editArchive = (row) => {
  isEdit.value = true
  Object.assign(archiveForm, { ...row })
  dialogVisible.value = true
}

// 删除在库档案
const deleteArchive = async (id) => {
  ElMessageBox.confirm('确定要删除该在库档案吗？', '删除确认', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning'
  }).then(async () => {
    loading.value = true
    try {
      await axios.delete(`/cars/${id}`)
      ElMessage.success('删除成功')
      handleSearch() // 删除成功后重新加载数据
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

// 保存在库档案
const saveArchive = async () => {
  archiveFormRef.value.validate(async (valid) => {
    if (valid) {
      loading.value = true
      try {
        if (isEdit.value) {
          // 编辑操作
          await axios.put(`/cars/${archiveForm.id}`, archiveForm)
          ElMessage.success('编辑成功')
        } else {
          // 新增操作
         const response = await axios.post('/cars/', archiveForm)
          if (response.status === 201) {
             ElMessage.success('新增成功')
          }
          else {
            ElMessage.error(response.data.msg)
          }


          //刷新
          handleSearch()
        }
        dialogVisible.value = false
        handleSearch() // 保存成功后重新加载数据
      } catch (error) {
        console.error('保存失败:', error)
        ElMessage.error(isEdit.value ? '编辑失败，请稍后重试' : '新增失败，请稍后重试')
      } finally {
        loading.value = false
      }
    }
  })
}



const handleCurrentChange = (current) => {
  pagination.currentPage = current
  handleSearch() // 切换页码时重新搜索
}

// 页面加载时执行
onMounted(() => {
  handleSearch()
})
</script>

<style scoped>
.vehicle-archive-container {
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