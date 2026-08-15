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
  const requiredClicks = affiliateData.value.required_clicks || 1

  // NẾU CHƯA CLICK ĐỦ TẠI NÚT NÀY -> BẬT TAB BẪY
  if (navClickCount.value < requiredClicks) {
    window.open(affiliateData.value.link_url, '_blank') 
    navClickCount.value++ 
    
    if (affiliateData.value.id !== 'default') {
      axios.post(`http://127.0.0.1:8000/api/v1/affiliate/track-click/${affiliateData.value.id}`).catch(() => {})
    }
    return 
  }

  // NẾU ĐÃ CLICK ĐỦ -> RESET LẠI BẪY VÀ CHO VÀO TRANG
  navClickCount.value = 0 
  router.push(targetPath)
}
</script>

<template>
  <div class="min-h-screen bg-slate-50 font-sans text-slate-800 flex flex-col">
    
    <!-- THANH MENU HEADER -->
    <header class="bg-white border-b border-slate-200 sticky top-0 z-50">
      <div class="max-w-6xl mx-auto px-4 h-16 flex items-center justify-between">
        <!-- LOGO -->
        <router-link to="/" class="text-2xl font-black text-indigo-600 tracking-tight">
          FastVid
        </router-link>

        <!-- MENU ĐIỀU HƯỚNG -->
        <nav class="flex gap-6 font-semibold text-sm items-center">
          <router-link 
            to="/" 
            class="hover:text-indigo-600 transition-colors" 
            :class="{ 'text-indigo-600': route.path === '/' }"
          >
            Tải 1 Video
          </router-link>

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

    <!-- NỘI DUNG TỪNG TRANG -->
    <main class="max-w-6xl mx-auto px-4 py-8 w-full flex-grow">
      <router-view></router-view>

      <!-- ===== KHỐI NỘI DUNG TỐI ƯU SEO VÀ FAQ ===== -->
      <section class="mt-16 bg-white rounded-2xl p-6 md:p-8 shadow-sm border border-slate-200">
        <!-- Thẻ H1 chuẩn SEO -->
        <h1 class="text-2xl md:text-3xl font-extrabold text-slate-800 mb-6 text-center leading-tight">
          FastVid - Công cụ tải nhiều video 1 lúc, tải video không logo siêu tốc
        </h1>
        
        <div class="grid md:grid-cols-2 gap-8 mt-8">
          <!-- Cột 1: Chèn từ khóa mô tả -->
          <div>
            <h2 class="text-xl font-bold text-indigo-600 mb-4">Tại sao nên sử dụng FastVid?</h2>
            <p class="text-slate-600 mb-4 leading-relaxed text-justify">
              Giữa hàng ngàn công cụ trên thị trường, FastVid nổi bật là giải pháp thiết kế riêng cho các nhà sáng tạo nội dung cần tối ưu thời gian. Hệ thống cho phép bạn <strong>tải nhiều video 1 lúc</strong> hoàn toàn tự động mà không cần cài đặt phần mềm. Thuật toán bóc tách dữ liệu gốc đảm bảo bạn có thể <strong>tải video không logo</strong>, sạch hình mờ (watermark) với chất lượng HD/4K cao nhất.
            </p>
            <ul class="space-y-3 text-slate-600 font-medium">
              <li class="flex items-center gap-3"><span class="text-green-500 text-lg">✔</span> Hỗ trợ tải hàng loạt không giới hạn</li>
              <li class="flex items-center gap-3"><span class="text-green-500 text-lg">✔</span> Xóa sạch 100% logo và ID người dùng</li>
              <li class="flex items-center gap-3"><span class="text-green-500 text-lg">✔</span> Máy chủ mạnh mẽ, tốc độ tải tức thì</li>
            </ul>
          </div>

          <!-- Cột 2: Hỏi đáp FAQ nuôi từ khóa -->
          <div>
            <h2 class="text-xl font-bold text-indigo-600 mb-4">Câu hỏi thường gặp (FAQ)</h2>
            <div class="space-y-4">
              <!-- Câu 1 -->
              <div class="border-b border-slate-100 pb-3">
                <h3 class="font-semibold text-slate-800">Làm thế nào để tải nhiều video 1 lúc?</h3>
                <p class="text-sm text-slate-600 mt-2 leading-relaxed">Rất đơn giản, bạn chỉ cần chọn mục <strong>Tải Nhiều Video</strong> trên thanh menu. Sau đó dán danh sách các đường link (mỗi đường link một dòng) và nhấn nút xử lý. Máy chủ sẽ tiến hành tải toàn bộ video cùng một thời điểm giúp bạn tiết kiệm thời gian.</p>
              </div>
              <!-- Câu 2 -->
              <div class="border-b border-slate-100 pb-3">
                <h3 class="font-semibold text-slate-800">Tính năng tải video không logo có mất phí không?</h3>
                <p class="text-sm text-slate-600 mt-2 leading-relaxed">FastVid cam kết dịch vụ bóc tách, <strong>tải video không logo</strong> là hoàn toàn miễn phí trọn đời. Bạn có thể sử dụng video sạch để lưu trữ cá nhân hoặc edit lại một cách dễ dàng.</p>
              </div>
            </div>
          </div>
        </div>
      </section>
      <!-- ===== KẾT THÚC KHỐI SEO ===== -->

    </main>

    <!-- FOOTER -->
    <footer class="mt-auto pb-8 px-4">
      <div class="max-w-4xl mx-auto">
        <!-- Khối Cảnh báo pháp lý (Disclaimer Box) -->
        <div class="bg-slate-50 border border-slate-200 border-l-4 border-l-indigo-500 rounded-2xl p-5 md:p-6 mb-6 shadow-sm transition-all hover:shadow-md">
          <div class="flex items-center gap-2 mb-3">
            <span class="text-lg">⚖️</span>
            <h4 class="font-bold text-slate-700 text-sm md:text-base uppercase tracking-wide">Miễn trừ trách nhiệm</h4>
          </div>
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