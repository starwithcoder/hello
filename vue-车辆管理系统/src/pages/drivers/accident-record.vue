<template>
  <div class="accident-record-container">
    <el-card shadow="hover" class="page-card">
      <template #header>
        <div class="card-header">
          <span class="header-title">事故记录管理</span>
          <el-button type="primary" @click="addRecord">
            <el-icon>
              <Plus/>
            </el-icon>
            新增事故记录
          </el-button>
        </div>
      </template>

      <!-- 搜索和筛选区域 -->
      <el-form :inline="true" class="search-form" label-width="80px">
        <el-form-item label="司机姓名">
          <el-input v-model="searchForm.driver_name" placeholder="请输入司机姓名" clearable/>
        </el-form-item>
        <el-form-item label="车牌号">
          <el-input v-model="searchForm.plate_number" placeholder="请输入车牌号" clearable/>
        </el-form-item>
        <el-form-item label="发生日期">
          <el-date-picker
              v-model="searchForm.occurrence_date"
              type="date"
              placeholder="选择发生日期"
              style="width: 180px"
          />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleSearch">搜索</el-button>
          <el-button @click="resetSearch">重置</el-button>
        </el-form-item>
      </el-form>

      <!-- 事故记录列表 -->
      <el-table
          :data="recordList"
          stripe
          border
          style="width: 100%"
          :row-key="row => row.id"
          v-loading="loading"
      >
        <el-table-column type="selection" width="55"/>
        <el-table-column prop="id" label="ID" width="80" align="center"/>
        <el-table-column prop="occurrence_date" label="发生日期" min-width="150"/>
        <el-table-column prop="driver_name" label="司机姓名" min-width="120"/>
        <el-table-column prop="plate_number" label="车牌号" min-width="120"/>
        <el-table-column prop="liability_determination" label="责任认定" min-width="120">
          <template #default="scope">
            <el-tag
                :type="scope.row.liability_determination === 'primary' ? 'danger' : scope.row.liability_determination === 'secondary' ? 'warning' : 'info'">
              {{ getResponsibilityText(scope.row.liability_determination) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="case_number" label="案件号" min-width="150"/>
        <el-table-column prop="remarks" label="备注" min-width="200" show-overflow-tooltip/>
        <el-table-column label="操作" width="150" align="center" fixed="right">
          <template #default="scope">
            <el-button type="primary" size="small" @click="editRecord(scope.row)">
              <el-icon>
                <Edit/>
              </el-icon>
              编辑
            </el-button>
            <el-button type="danger" size="small" @click="deleteRecord(scope.row.id)">
              <el-icon>
                <Delete/>
              </el-icon>
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

    <!-- 新增/编辑事故记录对话框 -->
    <el-dialog
        v-model="dialogVisible"
        :title="isEdit ? '编辑事故记录' : '新增事故记录'"
        width="600px"
         @close="handleClose"
>

    >
      <el-form :model="recordForm" :rules="recordRules" ref="recordFormRef" label-width="100px">
        <el-form-item label="发生日期" prop="occurrence_date">
          <el-date-picker
              v-model="recordForm.occurrence_date"
              value-format="YYYY-MM-DD HH:mm:ss"
              type="date"
              placeholder="选择发生日期"
              style="width: 100%"
          />
        </el-form-item>
        <el-form-item label="司机姓名" prop="driver_name">
          <el-input v-model="recordForm.driver_name" placeholder="请输入司机姓名"/>
        </el-form-item>
        <el-form-item label="车牌号" prop="plate_number">
          <el-input v-model="recordForm.plate_number" placeholder="请输入车牌号"/>
        </el-form-item>
        <el-form-item label="责任认定" prop="liability_determination">
          <el-select v-model="recordForm.liability_determination" placeholder="请选择责任认定">
             <el-option
      v-for="item in liabilityOptions"
      :key="item.value"
      :label="item.label"
      :value="item.value"
    />
          </el-select>
        </el-form-item>
        <el-form-item label="事故图" prop="accident_image_1">
          <el-upload
              v-model:file-list="accident_images"
              action="#"
              list-type="picture-card"
              :auto-upload="false"
              limit="4"
          >
          </el-upload>
        </el-form-item>
        <el-form-item label="案件号" prop="case_number">
          <el-input v-model="recordForm.case_number" placeholder="请输入案件号"/>
        </el-form-item>
        <el-form-item label="备注" prop="remarks">
          <el-input
              v-model="recordForm.remarks"
              type="textarea"
              :rows="3"
              placeholder="请输入备注"
          />
        </el-form-item>
      </el-form>
      <template #footer>
        <div class="dialog-footer">
          <el-button @click="dialogVisible = false">取消</el-button>
          <el-button type="primary" @click="saveRecord">保存</el-button>
        </div>
      </template>
    </el-dialog>

    <!-- 图片预览对话框 -->

  </div>
</template>

<script setup>
import {ref, reactive, onMounted} from 'vue'
import {Plus, Edit, Delete, ZoomIn} from '@element-plus/icons-vue'
import {ElMessageBox, ElMessage} from 'element-plus'
import axios from 'axios'



const liabilityOptions = [
  { label: '全责', value: 'primary' },
  { label: '主责', value: 'secondary' },
  { label: '同等责任', value: 'equal' },
  { label: '次责', value: 'minor' },
  { label: '无责', value: 'none' }
]

// 搜索表单
const searchForm = reactive({
  driver_name: '',
  plate_number: '',
  occurrence_date: ''
})

// 事故记录列表
const recordList = ref([])

// 加载状态
const loading = ref(false)

// 分页配置
const pagination = reactive({
  currentPage: 1,
  pageSize: 10,
  total: 2
})

// 对话框配置
const dialogVisible = ref(false)
const isEdit = ref(false)
const recordFormRef = ref(null)
const dialogImageUrl = ref('')

// 事故记录表单
const recordForm = reactive({
  id: '',
  occurrence_date: '',
  driver_name: '',
  plate_number: '',
  liability_determination: '',
  case_number: '',
  remarks: ''
})
//事故图片
const accident_images = ref([])

// 表单验证规则
const recordRules = {
  occurrence_date: [
    {required: false, message: '请选择发生日期', trigger: 'change'}
  ],
  driver_name: [
    {required: false, message: '请输入司机姓名', trigger: 'blur'}
  ],
  plate_number: [
    {required: false, message: '请输入车牌号', trigger: 'blur'}
  ],
  liability_determination: [
    {required: false, message: '请选择责任认定', trigger: 'change'}
  ],
  case_number: [
    {required: false, message: '请输入案件号', trigger: 'blur'}
  ]
}

// 获取责任认定文本
const getResponsibilityText = (responsibility) => {
  const responsibilityMap = {
    primary: '全责',
    secondary: '主责',
    equal: '同等责任',
    minor: '次责',
    none: '无责'
  }
  return responsibilityMap[responsibility] || responsibility
}

// 处理图片预览
const handlePictureCardPreview = (file) => {
  dialogImageUrl.value = file.url
}

// 处理图片删除
const handleRemove = (file, imageIndex) => {
  const imageKey = `accident_image_${imageIndex}`
  const index = recordForm[imageKey].findIndex(item => item.uid === file.uid)
  if (index !== -1) {
    recordForm[imageKey].splice(index, 1)
  }
}

// 搜索事故记录
const handleSearch = async () => {
  loading.value = true
  try {
    const response = await axios.get('/accident_record/', {
      params: {...searchForm, page: pagination.currentPage, page_size: pagination.pageSize}
    })
    recordList.value = response.data
    pagination.total = response.length
  } catch (error) {
    console.error('获取事故记录失败:', error)
    ElMessage.error('获取事故记录失败，请稍后重试')
  } finally {
    loading.value = false
  }
}

// 重置搜索
const resetSearch = () => {
  Object.assign(searchForm, {
    driver_name: '',
    plate_number: '',
    occurrence_date: ''
  })
  handleSearch()
}

// 新增事故记录
const addRecord = () => {
  isEdit.value = false
  dialogVisible.value = true
}
//关闭清空数据
const handleClose =()=>{
  Object.assign(recordForm, {
    id: '',
    occurrence_date: '',
    driver_name: '',
    plate_number: '',
    liability_determination: '',
    case_number: '',
    remarks: ''
  })
  accident_images.value = []

}
// 编辑事故记录
const editRecord = (row) => {
  isEdit.value = true
  Object.assign(recordForm, {...row})
  dialogVisible.value = true
}

// 删除事故记录
const deleteRecord = async (id) => {
  try {
    await ElMessageBox.confirm('确定要删除该事故记录吗？', '删除确认', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })

    loading.value = true
    await axios.delete(`/accident_record/${id}`)
    ElMessage.success('删除成功')
    handleSearch() // 重新加载数据
  } catch (error) {
    if (error !== 'cancel') {
      console.error('删除事故记录失败:', error)
      ElMessage.error('删除失败')
    }
  } finally {
    loading.value = false
  }
}

// 保存事故记录
const saveRecord = () => {
  recordFormRef.value.validate(async (valid) => {
    if (valid) {
      loading.value = true
      try {
        if (isEdit.value) {
          // 编辑事故记录
          await axios.put(`/accident_record/${recordForm.id}`, recordForm)
          ElMessage.success('编辑成功')
        } else {
          // 新增事故记录
          const formData = new FormData()

          accident_images.value.forEach((file,index) => {
              if(file.raw instanceof File )
                formData.append(`accident_images_${index+1}`, file.raw ??'' )
            })
          for (const [key,value] of Object.entries(recordForm)) {
            formData.append(key,value ?? '')
            console.log(key,value)
          }

          //console.log(formData.values())

          await axios.post('/accident_record/', formData)
          ElMessage.success('新增成功')
        }
        dialogVisible.value = false
        handleSearch() // 重新加载数据
      } catch (error) {
        console.error('保存事故记录失败:', error)
        ElMessage.error(isEdit.value ? '编辑失败' : '新增失败')
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
  handleSearch() // 重新搜索
}

const handleCurrentChange = (current) => {
  pagination.currentPage = current
  handleSearch() // 重新搜索
}

// 页面加载时执行
onMounted(() => {
  handleSearch()
})
</script>

<style scoped>
.accident-record-container {
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

:deep(.el-upload-list__item) {
  margin-bottom: 10px;
}
</style>