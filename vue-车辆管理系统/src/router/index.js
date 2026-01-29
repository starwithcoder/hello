import { createMemoryHistory, createRouter, createWebHashHistory, createWebHistory } from 'vue-router'

import  Index from '~/pages/index.vue'
import  About from '~/pages/about.vue'
import  NotFound from '~/pages/404.vue' 
import  Login from '~/pages/login.vue'
import  Register from '~/pages/register.vue'

import  Users from '~/pages/users.vue'
import  Drivers from '~/pages/drivers.vue'

import  MainLayout from '~/components/Layout/MainLayout.vue'

import  VehicleDynamic from '~/pages/drivers/vehicle-dynamic.vue'

import  DriverReturn from '~/pages/drivers/driver-return.vue'
import  VehicleChange from '~/pages/drivers/vehicle-change.vue'
import  Cars from '~/pages/drivers/Cars.vue'
import  AccidentRecord from '~/pages/drivers/accident-record.vue'
import  Primary from '~/pages/primary.vue'
import  Settings from '~/pages/settings.vue'
import  Permission from '~/pages/permission/Permission.vue'
import Role from "~/pages/role/Role.vue";
import It from '~/pages/it/It.vue'
import CarReceiptRecord from "~/pages/drivers/CarReceiptRecord.vue";



const routes = [
 { 
    path: '/', // 父路由：根路径
    component: MainLayout,
    meta: { requiresAuth: true },
    children: [
      // 子路由用「相对路径」（去掉开头的 /）
      { path: 'drivers', component: Drivers, meta: { requiresAuth: true } },  // 匹配 /drivers → 渲染 Drivers
      { path: 'users', component: Users, meta: { requiresAuth: true } }, // 匹配 /users → 渲染 Users
      { path: 'vehicle-dynamic', component: VehicleDynamic, meta: { requiresAuth: true } }, // 匹配 /vehicle-dynamic → 渲染 VehicleDynamic
      { path: 'carReceiptRecord', component: CarReceiptRecord, meta: { requiresAuth: true } }, // 匹配 /vehicle-recall → 渲染 VehicleRecall
      { path: 'driver-return', component: DriverReturn, meta: { requiresAuth: true } }, // 匹配 /driver-return → 渲染 DriverReturn
      { path: 'vehicle-change', component: VehicleChange, meta: { requiresAuth: true } }, // 匹配 /vehicle-change → 渲染 VehicleChange
      { path: 'cars', component: Cars, meta: { requiresAuth: true } }, // 匹配 /vehicle-archive → 渲染 Cars
      { path: 'accident-record', component: AccidentRecord, meta: { requiresAuth: true } }, // 匹配 /accident-record → 渲染 AccidentRecord
        {path: 'permissions', component: Permission, meta: { requiresAuth: true } },
        {path:'roles', component: Role, meta: { requiresAuth: true } },
        {path:'it', component: It, meta: { requiresAuth: true } },
    ]
  },
  { path: '/profile', component: Primary, meta: { requiresAuth: true } }, // 匹配 /profile → 渲染 Primary
  { path: '/', component: Login }, // 根路径 → 渲染 Login
  { path: '/login', component: Login }, // 一级路由：/login（无需登录）
  { path: '/about', component: About }, // 一级路由：/about（无需登录）
  { path: '/register', component: Register }, // 一级路由：/register（无需登录）
  { path: '/settings', component: Settings }, // 一级路由：/settings（无需登录）
  { path: '/:pathMatch(.*)*', component: NotFound } // 404路由：必须放最后！
]


const router = createRouter({
  history: createWebHashHistory(),
  routes,
})

// 路由拦截：登录验证
router.beforeEach((to, from, next) => {
  // 检查路由是否需要认证
  if (to.matched.some(record => record.meta.requiresAuth)) {
    // 检查是否已登录
    const isLoggedIn = localStorage.getItem('isLoggedIn') === 'true'
    if (!isLoggedIn) {
      // 未登录，重定向到登录页面
      next('/login')
    } else {
      // 已登录，继续访问
      next()
    }
  } else {
    // 不需要认证，直接访问
    next()
  }
})

export default router