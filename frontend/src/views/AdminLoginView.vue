<template>
  <div class="flex items-center justify-center min-h-screen bg-gray-900 text-white">
    <div class="w-full max-w-md p-8 space-y-6 bg-gray-800 rounded-lg shadow-xl border border-gray-700">
      <div class="text-center">
        <h2 class="text-2xl font-bold tracking-wider">QUẢN TRỊ HỆ THỐNG</h2>
        <p class="text-sm text-gray-400 mt-1">Vui lòng đăng nhập để tiếp tục</p>
      </div>

      <form @submit.prevent="handleLogin" class="space-y-4">
        <div>
          <label class="block text-sm font-medium text-gray-300">Tài khoản</label>
          <input 
            v-model="username" 
            type="text" 
            required 
            placeholder="Nhập tên đăng nhập"
            class="w-full px-4 py-2 mt-1 bg-gray-700 border border-gray-600 rounded focus:outline-none focus:border-blue-500 text-white"
          />
        </div>

        <div>
          <label class="block text-sm font-medium text-gray-300">Mật khẩu</label>
          <input 
            v-model="password" 
            type="password" 
            required 
            placeholder="••••••••"
            class="w-full px-4 py-2 mt-1 bg-gray-700 border border-gray-600 rounded focus:outline-none focus:border-blue-500 text-white"
          />
        </div>

        <div v-if="errorMessage" class="p-3 text-sm text-red-400 bg-red-900/40 border border-red-700 rounded">
          {{ errorMessage }}
        </div>

        <button 
          type="submit" 
          class="w-full py-2.5 font-semibold text-white bg-blue-600 rounded hover:bg-blue-700 transition duration-200 shadow-md"
        >
          Đăng Nhập
        </button>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const username = ref('')
const password = ref('')
const errorMessage = ref('')
const router = useRouter()

const handleLogin = async () => {
  errorMessage.value = ''
  try {
    const response = await fetch('/api/v1/auth/admin-login', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ 
        username: username.value, 
        password: password.value 
      })
    })
    
    const data = await response.json()
    
    if (response.ok && data.success) {
      // Lưu trạng thái đăng nhập vào localStorage
      localStorage.setItem('admin_logged', 'true')
      localStorage.setItem('admin_username', data.username)
      
      // Chuyển hướng vào trang quản trị chính
      router.push('/admin')
    } else {
      errorMessage.value = data.detail || 'Tài khoản hoặc mật khẩu không chính xác!'
    }
  } catch (err) {
    errorMessage.value = 'Không thể kết nối đến máy chủ backend!'
  }
}
</script>