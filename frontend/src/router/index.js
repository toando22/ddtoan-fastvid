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
  { 
    path: '/admin', 
    name: 'Admin',
    component: () => import('../views/AdminDashboardView.vue') 
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router