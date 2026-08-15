<script setup>
import { ref, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import axios from 'axios'

const router = useRouter()
const route = useRoute()

// Biến lưu trữ dữ liệu Affiliate
const affiliateData = ref({ link_url: 'https://shopee.vn', required_clicks: 1, id: 'default' })

// KHAI BÁO BIẾN NÀY ĐỂ KHÔNG BỊ LỖI (Bộ đếm độc lập cho Menu)
const navClickCount = ref(0) 

// Lấy thông tin bẫy Link ngay khi load trang tổng
onMounted(async () => {
  try {
    const res = await axios.get('http://127.0.0.1:8000/api/v1/affiliate/active')
    affiliateData.value = res.data
  } catch (error) {
    console.error("Lỗi lấy dữ liệu Affiliate:", error)
  }
})

// --- THUẬT TOÁN BẪY NGAY TẠI CỬA (MENU NAV) ---
const navigateWithTrap = (targetPath) => {
  // Đã xóa sạch code sessionStorage thừa ở đây!
  const requiredClicks = affiliateData.value.required_clicks || 1

  // NẾU CHƯA CLICK ĐỦ TẠI NÚT NÀY -> BẬT TAB BẪY
  if (navClickCount.value < requiredClicks) {
    window.open(affiliateData.value.link_url, '_blank') 
    navClickCount.value++ // Tăng bộ đếm của riêng nút này lên 1
    
    if (affiliateData.value.id !== 'default') {
      axios.post(`http://127.0.0.1:8000/api/v1/affiliate/track-click/${affiliateData.value.id}`).catch(() => {})
    }
    return // Chặn đứng lại
  }

  // NẾU ĐÃ CLICK ĐỦ -> RESET LẠI BẪY VÀ CHO VÀO TRANG
  navClickCount.value = 0 
  router.push(targetPath)
}
</script>

<template>
  <div class="min-h-screen bg-slate-50 font-sans text-slate-800">
    
    <!-- THANH MENU HEADER -->
    <header class="bg-white border-b border-slate-200 sticky top-0 z-50">
      <div class="max-w-6xl mx-auto px-4 h-16 flex items-center justify-between">
        
        <!-- LOGO -->
        <router-link to="/" class="text-2xl font-black text-indigo-600 tracking-tight">
          FastVid
        </router-link>

        <!-- MENU ĐIỀU HƯỚNG -->
        <nav class="flex gap-6 font-semibold text-sm items-center">
          <!-- Link Tải 1 Video (Bình thường) -->
          <router-link 
            to="/" 
            class="hover:text-indigo-600 transition-colors" 
            :class="{ 'text-indigo-600': route.path === '/' }"
          >
            Tải 1 Video
          </router-link>

          <!-- NÚT TẢI HÀNG LOẠT (Đã bị gài bẫy) -->
          <button 
            @click="navigateWithTrap('/bulk')" 
            class="hover:text-indigo-600 transition-colors font-semibold" 
            :class="{ 'text-indigo-600': route.path === '/bulk' }"
          >
            Tải Nhiều Video
          </button>
        </nav>
      </div>
    </header>

    <!-- NỘI DUNG TỪNG TRANG SẼ HIỂN THỊ Ở ĐÂY -->
    <main class="max-w-6xl mx-auto px-4 py-8">
      <router-view></router-view>
    </main>

    <!-- FOOTER -->
    <!-- FOOTER -->
    <footer class="mt-16 pb-8 px-4">
      <div class="max-w-4xl mx-auto">
        
        <!-- Khối Cảnh báo pháp lý (Disclaimer Box) -->
        <div class="bg-slate-50 border border-slate-200 border-l-4 border-l-indigo-500 rounded-2xl p-5 md:p-6 mb-6 shadow-sm transition-all hover:shadow-md">
          
          <!-- Tiêu đề hộp -->
          <div class="flex items-center gap-2 mb-3">
            <span class="text-lg">⚖️</span>
            <h4 class="font-bold text-slate-700 text-sm md:text-base uppercase tracking-wide">Miễn trừ trách nhiệm</h4>
          </div>
          
          <!-- Nội dung -->
          <div class="text-slate-500 text-xs md:text-sm leading-relaxed space-y-2 text-justify md:text-left">
            <p>
              <strong>FastVid</strong> là công cụ hỗ trợ tải video phục vụ mục đích cá nhân. Người dùng tự chịu mọi trách nhiệm trước pháp luật về vấn đề bản quyền đối với các nội dung tải xuống.
            </p>
            <p>
              Chúng tôi không khuyến khích và <span class="text-red-500 font-semibold">không chịu trách nhiệm</span> cho các hành vi tải video để đăng tải lại (re-up) nhằm mục đích thương mại khi chưa có sự cho phép của tác giả gốc.
            </p>
          </div>

        </div>

        <!-- Khối Bản quyền -->
        <div class="text-center text-slate-400 text-sm font-medium">
          <p>&copy; 2026 FastVid - All rights reserved.</p>
        </div>

      </div>
    </footer>

  </div>
</template>