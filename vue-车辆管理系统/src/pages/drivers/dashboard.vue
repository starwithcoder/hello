<template>
  <div class="dashboard-page">
    <div class="page-header">
      <h1 class="page-title">仪表盘</h1>
      <p class="page-subtitle">欢迎回来，管理员</p>
    </div>
    
    <!-- 指标卡片 -->
    <div class="metrics-section">
      <el-row :gutter="20">
        <el-col :span="6">
          <el-card shadow="hover" class="metric-card">
            <template #header>
              <div class="card-header">
                <span>总用户数</span>
                <el-icon class="card-icon"><UserFilled /></el-icon>
              </div>
            </template>
            <el-statistic
              :value="totalUsers"
              :precision="0"
              value-style="{ fontSize: '24px', fontWeight: 'bold' }"
              suffix="人"
            >
              <template #prefix>
                <el-icon color="#10b981"><TrendCharts /></el-icon>
              </template>
            </el-statistic>
            <div class="metric-change">
              <span class="change-positive">+{{ userGrowthRate }}%</span>
              <span class="change-desc">较上月增长</span>
            </div>
          </el-card>
        </el-col>
        
        <el-col :span="6">
          <el-card shadow="hover" class="metric-card">
            <template #header>
              <div class="card-header">
                <span>总销售额</span>
                <el-icon class="card-icon"><Money /></el-icon>
              </div>
            </template>
            <el-statistic
              :value="totalSales"
              :precision="2"
              value-style="{ fontSize: '24px', fontWeight: 'bold' }"
              prefix="¥"
            >
              <template #prefix>
                <el-icon color="#3b82f6"><TrendCharts /></el-icon>
              </template>
            </el-statistic>
            <div class="metric-change">
              <span class="change-positive">+{{ salesGrowthRate }}%</span>
              <span class="change-desc">较上月增长</span>
            </div>
          </el-card>
        </el-col>
        
        <el-col :span="6">
          <el-card shadow="hover" class="metric-card">
            <template #header>
              <div class="card-header">
                <span>今日订单</span>
                <el-icon class="card-icon"><ShoppingCart /></el-icon>
              </div>
            </template>
            <el-statistic
              :value="todayOrders"
              :precision="0"
              value-style="{ fontSize: '24px', fontWeight: 'bold' }"
              suffix="笔"
            >
              <template #prefix>
                <el-icon color="#8b5cf6"><TrendCharts /></el-icon>
              </template>
            </el-statistic>
            <div class="metric-change">
              <span class="change-negative">{{ orderChangeRate }}%</span>
              <span class="change-desc">较昨日变化</span>
            </div>
          </el-card>
        </el-col>
        
        <el-col :span="6">
          <el-card shadow="hover" class="metric-card">
            <template #header>
              <div class="card-header">
                <span>产品总数</span>
                <el-icon class="card-icon"><Box /></el-icon>
              </div>
            </template>
            <el-statistic
              :value="totalProducts"
              :precision="0"
              value-style="{ fontSize: '24px', fontWeight: 'bold' }"
              suffix="种"
            >
              <template #prefix>
                <el-icon color="#f59e0b"><TrendCharts /></el-icon>
              </template>
            </el-statistic>
            <div class="metric-change">
              <span class="change-positive">+{{ productGrowthRate }}%</span>
              <span class="change-desc">较上月增长</span>
            </div>
          </el-card>
        </el-col>
      </el-row>
    </div>
    
    <!-- 图表和数据区域 -->
    <div class="data-section">
      <el-row :gutter="20">
        <el-col :span="16">
          <el-card shadow="hover" class="chart-card">
            <template #header>
              <div class="card-header">
                <span>销售趋势</span>
              </div>
            </template>
            <div class="chart-container">
              <!-- 这里可以集成 ECharts 或其他图表库 -->
              <div class="chart-placeholder">
                <el-icon class="placeholder-icon"><DataAnalysis /></el-icon>
                <p>销售趋势图表</p>
              </div>
            </div>
          </el-card>
        </el-col>
        
        <el-col :span="8">
          <el-card shadow="hover" class="chart-card">
            <template #header>
              <div class="card-header">
                <span>用户分布</span>
              </div>
            </template>
            <div class="chart-container">
              <!-- 这里可以集成 ECharts 或其他图表库 -->
              <div class="chart-placeholder">
                <el-icon class="placeholder-icon"><PieChart /></el-icon>
                <p>用户分布图表</p>
              </div>
            </div>
          </el-card>
        </el-col>
      </el-row>
    </div>
    
    <!-- 最近活动 -->
    <div class="activities-section">
      <el-card shadow="hover" class="activities-card">
        <template #header>
          <div class="card-header">
            <span>最近活动</span>
            <el-button type="text" size="small">查看全部</el-button>
          </div>
        </template>
        <el-table :data="recentActivities" stripe border style="width: 100%">
          <el-table-column prop="time" label="时间" width="180"></el-table-column>
          <el-table-column prop="user" label="用户" width="120"></el-table-column>
          <el-table-column prop="action" label="操作" min-width="200"></el-table-column>
          <el-table-column prop="status" label="状态" width="100">
            <template #default="scope">
              <el-tag
                :type="scope.row.status === 'success' ? 'success' : 'warning'"
                size="small"
              >
                {{ scope.row.status === 'success' ? '成功' : '失败' }}
              </el-tag>
            </template>
          </el-table-column>
        </el-table>
      </el-card>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import {
  UserFilled,
  Money,
  ShoppingCart,
  Box,
  TrendCharts,
  DataAnalysis,
  PieChart
} from '@element-plus/icons-vue'

// 模拟数据
const totalUsers = ref(12580)
const userGrowthRate = ref(15.2)
const totalSales = ref(856903.56)
const salesGrowthRate = ref(8.7)
const todayOrders = ref(234)
const orderChangeRate = ref(-2.1)
const totalProducts = ref(896)
const productGrowthRate = ref(12.5)

const recentActivities = ref([
  { time: '2025-12-14 14:30', user: '张三', action: '登录系统', status: 'success' },
  { time: '2025-12-14 14:15', user: '李四', action: '创建了新订单 #20251214001', status: 'success' },
  { time: '2025-12-14 13:50', user: '王五', action: '修改了用户信息', status: 'success' },
  { time: '2025-12-14 13:20', user: '赵六', action: '删除了产品 ID: P00123', status: 'success' },
  { time: '2025-12-14 12:45', user: '钱七', action: '登录系统', status: 'failed' }
])
</script>

<style scoped>
.dashboard-page {
  width: 100%;
  height: 100%;
}

.page-header {
  margin-bottom: 30px;
}

.page-title {
  font-size: 28px;
  font-weight: bold;
  margin: 0 0 8px 0;
  color: #303133;
}

.page-subtitle {
  font-size: 14px;
  color: #909399;
  margin: 0;
}

.metrics-section {
  margin-bottom: 20px;
}

.metric-card {
  height: 100%;
  transition: transform 0.3s ease;
}

.metric-card:hover {
  transform: translateY(-2px);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-weight: 500;
  color: #606266;
}

.card-icon {
  color: #409EFF;
  font-size: 18px;
}

.metric-change {
  margin-top: 10px;
  font-size: 12px;
}

.change-positive {
  color: #10b981;
  font-weight: 500;
  margin-right: 5px;
}

.change-negative {
  color: #ef4444;
  font-weight: 500;
  margin-right: 5px;
}

.change-desc {
  color: #909399;
}

.data-section {
  margin-bottom: 20px;
}

.chart-card {
  height: 100%;
}

.chart-container {
  height: 300px;
  display: flex;
  justify-content: center;
  align-items: center;
}

.chart-placeholder {
  display: flex;
  flex-direction: column;
  align-items: center;
  color: #909399;
}

.placeholder-icon {
  font-size: 48px;
  margin-bottom: 10px;
  opacity: 0.5;
}

.activities-section {
  margin-bottom: 20px;
}
</style>