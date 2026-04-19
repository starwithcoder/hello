<template>
  <!-- 删掉多余的 el-col，只保留一个；el-row 可保留（也可直接删，不影响） -->
  <el-row class="tac">
    <el-col :span="12"> <!-- 若想让侧边栏占满宽度，可把 :span="12" 改成 :span="24" -->
      <h5 class="mb-2">车辆管理系统</h5>

      <el-menu
          default-active="2"
          class="el-menu-vertical-demo"
          router="true"
          @open="handleOpen"
          @close="handleClose"
      >
        <!-- 司机信息管理*************************************** -->
        <el-menu-item index="drivers" v-if="isdrivers">
          <el-icon>
            <User/>
          </el-icon>
          <span>司机信息管理</span>
        </el-menu-item>

        <!-- 汽车在库档案管理********************************** -->
        <el-menu-item index="cars" v-if="iscars">
          <el-icon>
            <Box/>
          </el-icon>
          <span>汽车在库档案管理</span>
        </el-menu-item>
        <!-- 记录************************************** -->
        <el-sub-menu index="records" v-if="isrecords">
          <!-- 这里使用了具名插槽来定义菜单标题 -->
          <template #title>
            <el-icon>
              <Document/>
            </el-icon>
            <span>记录</span>
          </template>

          <!-- 换车记录 -->
          <el-menu-item index="vehicle-change">
            <el-icon>
              <RefreshRight/>
            </el-icon>
            <span>换车记录</span>
          </el-menu-item>

          <!-- 司机退车 -->
          <el-menu-item index="driver-return">
            <el-icon>
              <CaretLeft/>
            </el-icon>
            <span>司机退车</span>
          </el-menu-item>

          <!-- 收车记录 -->
          <el-menu-item index="carReceiptRecord">
            <el-icon>
              <RefreshRight/>
            </el-icon>
            <span>收车记录</span>
          </el-menu-item>
        </el-sub-menu>

        <!-- 事故 (下拉菜单) ***************************************-->
        <el-sub-menu index="accident" v-if="isaccident">
          <template #title>
            <el-icon>
              <WarningFilled/>
            </el-icon>
            <span>事故</span>
          </template>

          <!-- 事故记录管理 -->
          <el-menu-item index="accident-record">
            <el-icon>
              <WarningFilled/>
            </el-icon>
            <span>事故记录管理</span>
          </el-menu-item>

          <!-- 车辆动态管理 -->
          <el-menu-item index="vehicle-dynamic">
            <el-icon>
              <Van/>
            </el-icon>
            <span>车辆动态管理</span>
          </el-menu-item>
        </el-sub-menu>

        <!-- 其他********************************************** -->
        <el-menu-item index="it" v-if="isit">
          <el-icon>
            <Setting/>
          </el-icon>
          <span>其他</span>
        </el-menu-item>
      </el-menu>
    </el-col>
  </el-row>
</template>

<script lang="ts" setup>
import {
  Document,
  Menu as IconMenu, // 别名 IconMenu，模板中要对应
  Location,
  Setting,
  User,

  Box,
  WarningFilled,
  RefreshRight,
  Van,
  CaretLeft
} from '@element-plus/icons-vue'
import {onMounted, reactive, ref} from "vue";

const isit = ref(false);
const isaccident = ref(false);
const iscars = ref(false);
const isdrivers = ref(false);
const isrecords = ref(false);

import {jwtDecode} from 'jwt-decode';

const token = localStorage.getItem('token')

const payload = jwtDecode(token);

console.log(payload)


// 修正 keyPath 类型（Element Plus 实际是 (string | number)[]，避免 TS 报错）
const handleOpen = (key: string | number, keyPath: (string | number)[]) => {
  console.log(key, keyPath)
}
const handleClose = (key: string | number, keyPath: (string | number)[]) => {
  console.log(key, keyPath)
}

//这里通过权限判断来控制是否显示IT菜单
//默认设置五个权限分别是司机，汽车，记录，事故，其他，默认对应0，1，2，3，4
//
onMounted(() => {
  //由于开发与数据库原因以下代码注释，请自行修改，判断权限目前写死
  //const permissions = payload.permissions
  const permissions = [0, 1, 2, 3, 4]
  console.log("解析到的权限是"+permissions)

  if (permissions.includes(4)){
    //其他
    isit.value = true
  }
  if (permissions.includes(3)) {
    //事故
    isaccident.value = true
  }
  if (permissions.includes(2)) {
    //记录
    isrecords.value = true
  }
  if (permissions.includes(1)) {
    // 汽车
    iscars.value = true
  }
  if (permissions.includes(0)) {
    //司机
    isdrivers.value = true
  }
})
</script>

<!-- 可选：调整样式，让侧边栏更美观 -->
<style scoped>
.tac {
  padding: 20px;
}

.el-menu-vertical-demo {
  width: 200px; /* 固定侧边栏宽度 */
}


.custom-sidebar-menu {
  border: none;
  min-height: 100%;
  background-color: #ffffff;
  box-shadow: 2px 0 8px rgba(0, 0, 0, 0.06);
}

/* 菜单项通用样式 */
:deep(.custom-sidebar-menu .el-menu-item),
:deep(.custom-sidebar-menu .el-sub-menu__title) {
  height: 52px;
  line-height: 52px;
  font-size: 15px;
  padding: 0 24px !important;
  margin: 4px 0;
  border-radius: 8px;
  transition: all 0.25s ease;
}

/* 图标统一大小和间距 */
:deep(.custom-sidebar-menu .el-icon) {
  width: 20px;
  margin-right: 12px;
  font-size: 18px;
  color: #606266;
}

/* 悬停效果 */
:deep(.custom-sidebar-menu .el-menu-item:hover),
:deep(.custom-sidebar-menu .el-sub-menu__title:hover) {
  background-color: #f0f9ff !important;
  color: #409eff !important;
}
:deep(.custom-sidebar-menu .el-menu-item:hover .el-icon),
:deep(.custom-sidebar-menu .el-sub-menu__title:hover .el-icon) {
  color: #409eff !important;
}

/* 选中状态 */
:deep(.custom-sidebar-menu .el-menu-item.is-active) {
  background-color: #ecf5ff !important;
  color: #409eff !important;
  font-weight: 600;
}
:deep(.custom-sidebar-menu .el-menu-item.is-active .el-icon) {
  color: #409eff !important;
}

/* 子菜单项缩进 */
:deep(.custom-sidebar-menu .el-sub-menu .el-menu-item) {
  padding-left: 48px !important;
  background-color: transparent !important;
}
:deep(.custom-sidebar-menu .el-sub-menu .el-menu-item.is-active) {
  background-color: #eef7ff !important;
}
</style>




