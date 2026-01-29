<template>
  <div class="drivers-container">
    <el-card shadow="hover" class="page-card">
      <template #header>
        <div class="card-header">
          <span class="header-title">司机信息管理</span>
          <el-button type="primary" @click="addDriver">
            <el-icon>
              <Plus/>
            </el-icon>
            新增司机
          </el-button>
        </div>
      </template>

      <!-- 搜索和筛选区域 -->
      <el-form :inline="true" class="search-form" label-width="80px">
        <el-form-item label="司机姓名">
          <el-input v-model="searchForm.driver_name" placeholder="请输入司机姓名" clearable/>
        </el-form-item>
        <el-form-item label="手机号码">
          <el-input v-model="searchForm.driver_phone" placeholder="请输入手机号码" clearable/>
        </el-form-item>

        <el-form-item>
          <el-button type="primary" @click="handleSearch">搜索</el-button>
          <el-button @click="resetSearch">重置</el-button>
        </el-form-item>
      </el-form>

      <!-- 司机列表 -->
      <el-table
          :data="driversList"
          stripe
          border
          style="width: 100%"
          :row-key="row => row.id"
          v-loading="loading"
      >
        <el-table-column type="selection" width="55"/>
        <el-table-column prop="id" label="司机ID" width="80" align="center"/>
        <el-table-column prop="platform"  label="平台" width="80" align="center"/>
        <el-table-column prop="driver_name" label="司机姓名" min-width="120"/>
        <el-table-column prop="driver_phone" label="手机号码" min-width="150"/>
        <el-table-column prop="plate_numbers" label="车牌" min-width="150"/>
        <el-table-column prop="remarks" label="备注" min-width="180" show-overflow-tooltip/>
        <el-table-column label="操作" width="150" align="center" fixed="right">
          <template #default="scope">
            <el-button type="primary" size="small" @click="editDriver(scope.row)">
              <el-icon>
                <Edit/>
              </el-icon>
              编辑
            </el-button>
            <el-button type="danger" size="small" @click="deleteDriver(scope.row.driver_id)">
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

    <!-- 新增/编辑司机对话框 -->
    <el-dialog
        v-model="dialogVisible"
        :title="isEdit ? '编辑司机' : '新增司机'"
        width="500px"
    >
      <el-form :model="driverForm" :rules="driverRules" ref="driverFormRef" label-width="100px">
        <el-form-item label="司机姓名" prop="name">
          <el-input v-model="driverForm.name" placeholder="请输入司机姓名"/>
        </el-form-item>
         <el-form-item label="平台" prop="name">
          <el-input v-model="driverForm.platform" placeholder="请输入平台"/>
        </el-form-item>
        <el-form-item label="手机号码" prop="phone">
          <el-input v-model="driverForm.phone" placeholder="请输入手机号码"/>
        </el-form-item>
        <!-- 车牌号 -->
        <el-form-item v-if="isEdit" label="车牌号" prop="plateNumber">
          <el-select
              v-model="driverForm.plateNumber"
              filterable
              remote
              allow-create
              reserve-keyword
              placeholder="请输入车牌号"
              :remote-method="remoteSearchCars"
              :loading="carLoading"
              clearable

          >
            <el-option
                v-for="car in carOptions"
                :key="car.plate_number"
                :label="car.plate_number"
                :value="car.plate_number"
            />
          </el-select>

<!--           <el-input v-model="driverForm.plateNumber" placeholder="请输入车牌号"/>-->
        </el-form-item>
        <!-- 备注 -->
        <el-form-item label="备注" prop="remark">
          <el-input
              v-model="driverForm.remark"
              type="textarea"
              :rows="2"
              placeholder="请输入备注"
          />
        </el-form-item>
      </el-form>
      <template #footer>
        <div class="dialog-footer">
          <el-button @click="dialogVisible = false">取消</el-button>
          <el-button type="primary" @click="saveDriver" :loading="dialogLoading">保存</el-button>
        </div>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import {ref, reactive, onMounted} from 'vue'
import {Plus, Edit, Delete} from '@element-plus/icons-vue'
import axios from 'axios'
import {ElMessageBox, ElMessage} from 'element-plus'

// 搜索表单
const searchForm = reactive({
  driver_name: '',
  driver_phone: ''
})

// 司机列表
const driversList = ref([])

// 分页配置
const pagination = reactive({
  currentPage: 1,
  pageSize: 10,
  total: 0
})

// 对话框配置
const dialogVisible = ref(false)
const isEdit = ref(false)
const driverFormRef = ref(null)

// 加载状态
const loading = ref(false)
const dialogLoading = ref(false)

// 司机表单
const driverForm = reactive({
  platform: '',
  name: '',
  phone: '',
  licenseNumber: '',
  licenseType: '',
  plateNumber: '',
  carModel: '',
  remark: ''
})

// 表单验证规则
const driverRules = {
  name: [
    {required: true, message: '请输入司机姓名', trigger: 'blur'},
    {min: 2, max: 20, message: '长度在 2 到 20 个字符', trigger: 'blur'}
  ],
  phone: [
    {required: true, message: '请输入手机号码', trigger: 'blur'},
    {pattern: /^1[3-9]\d{9}$/, message: '请输入正确的手机号码', trigger: 'blur'}
  ],
  licenseNumber: [
    {required: true, message: '请输入平台', trigger: 'blur'}
  ],
  licenseType: [
    {required: true, message: '请输入车牌', trigger: 'blur'}
  ]
}

// 搜索司机
const handleSearch = async () => {
  loading.value = true
  try {
    const params = {
      page: pagination.currentPage,
      page_size: pagination.pageSize,
      ...searchForm
    }
    //如果有司机姓名或司机手机号，就搜索司机
    const url = searchForm.driver_name || searchForm.driver_phone ? '/drivers/search/' : '/drivers/'
    const response = await axios.get(url, {params})

    console.log(response.data.data)
    driversList.value = response.data.data


    // 如果后端返回total字段，则设置分页总数
    // pagination.total = response.data.total || 0
  } catch (error) {
    console.error('获取司机列表失败:', error)
    ElMessage.error('获取司机列表失败，请稍后重试')
  } finally {
    loading.value = false
  }
}


// 重置搜索
const resetSearch = () => {
  Object.assign(searchForm, {
    driver_name: '',
    driver_phone: ''
  })
  pagination.currentPage = 1
  handleSearch()
}

// 新增司机
const addDriver = () => {
  isEdit.value = false
  Object.assign(driverForm, {

    name: '',
    phone: '',
    licenseNumber: '',
    plateNumber: '',
    carModel: '',
    remark: ''
  })
  dialogVisible.value = true
}

// 编辑司机
const editDriver = (row) => {
  isEdit.value = true
  // 将后端返回的字段映射到前端表单字段
  Object.assign(driverForm, {
    platform_id: row.id,
    name: row.driver_name, // 司机姓名映射到name
    phone: row.driver_phone, // 司机手机号映射到phone
    licenseNumber: row.platform, // 平台映射到licenseNumber
    plateNumber: row.plate_number, // 车牌号映射到plateNumber
    carModel: row.vehicle_model, // 车型映射到carModel
    remark: row.remarks // 备注映射到remark
  })
  dialogVisible.value = true
}


// 删除司机
const deleteDriver = (driver_id) => {
  ElMessageBox.confirm('确定要删除该司机信息吗？', '删除确认', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning'
  }).then(async () => {
    try {
      await axios.delete(`/drivers/${driver_id}`)
      ElMessage.success('删除成功')
      handleSearch() // 重新加载列表
    } catch (error) {
      console.error('删除司机失败:', error)
      ElMessage.error('删除失败，请稍后重试')
    }
  }).catch(() => {
    // 取消删除
  })
}

// 保存司机
const saveDriver = async () => {
  if (!driverFormRef.value) return

  try {
    await driverFormRef.value.validate()
    dialogLoading.value = true

    // 构建与后端数据库字段匹配的数据结构
    const formData = {
      driver_name: driverForm.name, // 司机姓名映射自name
      driver_phone: driverForm.phone, // 司机手机号映射自phone
      plate_number: driverForm.plateNumber, // 车牌号映射自plateNumber
      remarks: driverForm.remark // 备注映射自remark
    }

    if (isEdit.value) {
      // 更新司机 - 添加id字段

      formData.platform_id = driverForm.platform_id
      console.log(formData)
      await axios.put(`/drivers/${formData.platform_id}`, formData)
      ElMessage.success('编辑成功')
      // 更新成功后刷新数据
      await handleSearch()
    } else {
      // 新增司机
      await axios.post('/drivers/', formData)
      ElMessage.success('新增成功')
    }

    dialogVisible.value = false
    handleSearch() // 重新加载列表
  } catch (error) {
    console.error('保存司机失败:', error)
    if (error.response) {
      ElMessage.error(error.response.data.message || '保存失败，请稍后重试')
    } else {
      ElMessage.error('网络异常，请检查网络连接')
    }
  } finally {
    dialogLoading.value = false
  }
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

//车牌号的搜索
const carOptions = ref([])        // 下拉选项列表
const carLoading = ref(false)     // 加载状态

    // 远程搜索车辆（防抖建议加，此处简化）
    const remoteSearchCars = async (query) =>{
        if (query === '') {
        carOptions.value = []
        return
      }
        try{
           // 调用你的后端接口，支持 ?q=粤B12345
        const res = await axios.get('/cars/search/plateNumber', {
          params: { q: query }
        })
        carOptions.value = res.data.data || []
      } catch (error) {
        console.error('搜索车辆失败:', error)
        carOptions.value = []
      } finally {
        carLoading.value = false
      }


    }


// 页面加载时执行
onMounted(() => {
  handleSearch()
})
</script>

<style scoped>
.drivers-container {
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