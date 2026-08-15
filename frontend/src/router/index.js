import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  { 
    path: '/', 
    name: 'Single',
    component: () => import('../views/SingleDownloadView.vue') 
  },
  { 
    path: '/bulk', 
    name: 'Bulk',
    component: () => import('../views/BulkDownloadView.vue') 
  },
  // BỔ SUNG TRANG ADMIN VÀO ĐÂY
// Thêm route giao diện đăng nhập Admin
  { 
    path: '/admin/login', 
    name: 'AdminLogin',
    component: () => import('../views/AdminLoginView.vue') 
  },
  // Route Admin được bảo vệ bởi Guard
  { 
    path: '/admin', 
    name: 'Admin',
    component: () => import('../views/AdminDashboardView.vue'),
    beforeEnter: (to, from, next) => {
      const isLoggedIn = localStorage.getItem('admin_logged') === 'true'
      if (isLoggedIn) {
        next() // Cho phép vào nếu đã đăng nhập
      } else {
        next('/admin/login') // Đá về trang đăng nhập nếu chưa có phiên
      }
    }  
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router