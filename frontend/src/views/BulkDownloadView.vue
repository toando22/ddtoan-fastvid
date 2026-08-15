<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

// --- TRẠNG THÁI BẢO MẬT VIP ---
const isAuthenticated = ref(false)
const passcode = ref('')
const authError = ref('')
const isVerifying = ref(false)

// --- TRẠNG THÁI TẢI HÀNG LOẠT ---
const bulkUrls = ref('')
const results = ref([])
const isLoading = ref(false)
const errorMsg = ref('')

// --- TRẠNG THÁI AFFILIATE BẪY ---
const affiliateData = ref({ link_url: 'https://shopee.vn', required_clicks: 1, id: 'default' })

// Lấy thông tin bẫy Link ngay khi vào trang
onMounted(async () => {
  try {
    const res = await axios.get('http://127.0.0.1:8000/api/v1/affiliate/active')
    affiliateData.value = res.data
  } catch (error) {
    console.error("Lỗi lấy dữ liệu Affiliate:", error)
  }
})

// --- HÀM 1: XÁC THỰC MÃ VIP ---
const verifyPasscode = async () => {
  if (!passcode.value) {
    authError.value = 'Vui lòng nhập mã truy cập'
    return
  }
  isVerifying.value = true
  authError.value = ''
  try {
    const res = await axios.post('http://127.0.0.1:8000/api/v1/auth/verify', { passcode: passcode.value })
    if (res.data.success) {
      isAuthenticated.value = true
    } else {
      authError.value = res.data.message || 'Mã không hợp lệ'
    }
  } catch (error) {
    authError.value = 'Lỗi kết nối máy chủ'
  } finally {
    isVerifying.value = false
  }
}

// BIẾN ĐẾM BẪY ĐỘC LẬP DÀNH RIÊNG CHO NÚT TẢI
const bulkClickCount = ref(0)

const handleBulkActionClick = async () => {
  if (!bulkUrls.value || bulkUrls.value.trim() === '') {
    errorMsg.value = 'Vui lòng dán danh sách link vào ô trống trước!'
    return
  }
  errorMsg.value = ''

  const requiredClicks = affiliateData.value.required_clicks || 1

  // NẾU CHƯA CLICK ĐỦ TẠI NÚT NÀY -> BẬT TAB BẪY
  if (bulkClickCount.value < requiredClicks) {
    window.open(affiliateData.value.link_url, '_blank') 
    bulkClickCount.value++ // Tăng biến đếm của riêng nút này
    
    if (affiliateData.value.id !== 'default') {
      axios.post(`http://127.0.0.1:8000/api/v1/affiliate/track-click/${affiliateData.value.id}`).catch(() => {})
    }
    return // Chặn tiến trình tải
  }

  // NẾU ĐÃ CLICK ĐỦ -> TIẾN HÀNH TẢI & RESET BẪY CHO LẦN SAU
  bulkClickCount.value = 0 
  processRealBulkDownload()
}

// --- HÀM 3: XỬ LÝ TẢI VIDEO HÀNG LOẠT ---
const processRealBulkDownload = async () => {
  isLoading.value = true
  errorMsg.value = ''
  results.value = []

  // Tách từng dòng link ra thành mảng
  const urls = bulkUrls.value.split('\n').filter(url => url.trim() !== '')
  
  if (urls.length === 0) {
    errorMsg.value = 'Không tìm thấy link hợp lệ nào.'
    isLoading.value = false
    return
  }

  // Gửi API lần lượt từng link để lấy dữ liệu
  for (const url of urls) {
    try {
      const response = await axios.post('http://127.0.0.1:8000/api/v1/download/extract', { url: url.trim() })
      if (response.data.success) {
        results.value.push({ original_url: url, ...response.data })
      } else {
        results.value.push({ original_url: url, error: response.data.error || 'Lỗi phân tích' })
      }
    } catch (error) {
      results.value.push({ original_url: url, error: 'Lỗi mạng khi phân tích' })
    }
  }

  // Ghi log tải thành công
  axios.post('http://127.0.0.1:8000/api/v1/logs/record', {
    action_type: 'BULK_DOWNLOAD',
    status_code: 200
  }).catch(() => {})

  isLoading.value = false
}
</script>

<template>
  <div class="max-w-4xl mx-auto">
    <!-- HEADER -->
    <div class="text-center mb-8">
      <h2 class="text-3xl font-extrabold text-slate-800">Tải Hàng Loạt VIP</h2>
      <p class="text-slate-500 mt-2">Dán nhiều link video để tải xuống cùng lúc (Bảo mật bằng Passcode)</p>
    </div>

    <!-- 1. FORM BẢO MẬT (Hiển thị nếu chưa nhập mã) -->
    <div v-if="!isAuthenticated" class="bg-white p-8 rounded-2xl shadow-sm border border-slate-200 max-w-md mx-auto">
      <h3 class="text-xl font-bold text-center text-slate-800 mb-4">Nhập Mã Truy Cập</h3>
      <input 
        v-model="passcode" 
        type="password" 
        placeholder="Nhập mã VIP..." 
        class="w-full px-4 py-3 border border-slate-300 rounded-xl mb-4 focus:ring-2 focus:ring-indigo-500 outline-none" 
        @keyup.enter="verifyPasscode"
      />
      <p v-if="authError" class="text-red-500 text-sm mb-4 text-center font-medium">{{ authError }}</p>
      
      <button 
        @click="verifyPasscode" 
        :disabled="isVerifying" 
        class="w-full bg-indigo-600 hover:bg-indigo-700 text-white font-bold py-3 rounded-xl transition-all shadow-md disabled:opacity-70"
      >
        {{ isVerifying ? 'Đang kiểm tra...' : 'MỞ KHÓA TÍNH NĂNG' }}
      </button>
    </div>

    <!-- 2. KHU VỰC LÀM VIỆC (Hiển thị sau khi nhập đúng mã) -->
    <div v-else class="space-y-6 animate-fade-in">
      
      <!-- Box Nhập Link -->
      <div class="bg-white p-6 rounded-2xl shadow-sm border border-slate-200">
        <label class="block text-sm font-semibold text-slate-700 mb-2">Danh sách Link (Mỗi link để trên 1 dòng):</label>
        <textarea 
          v-model="bulkUrls" 
          rows="6" 
          class="w-full p-4 border border-slate-300 rounded-xl focus:ring-2 focus:ring-indigo-500 outline-none resize-none font-mono text-sm bg-slate-50" 
          placeholder="https://vt.tiktok.com/...&#10;https://vn.shp.ee/..."
        ></textarea>
        <p v-if="errorMsg" class="text-red-500 text-sm mt-2 font-medium">{{ errorMsg }}</p>

        <!-- NÚT TẢI HÀNG LOẠT VỚI HIỆU ỨNG THU HÚT ÁNH NHÌN -->
        <button 
          @click="handleBulkActionClick"
          :disabled="isLoading"
          class="w-full mt-4 bg-gradient-to-r from-pink-500 via-red-500 to-yellow-500 hover:from-pink-600 hover:via-red-600 hover:to-yellow-600 text-white font-black text-lg md:text-xl py-4 px-8 rounded-2xl shadow-[0_0_20px_rgba(236,72,153,0.6)] transform hover:scale-[1.02] transition-all duration-300 animate-pulse hover:animate-none flex items-center justify-center gap-3 relative overflow-hidden group disabled:opacity-70 disabled:animate-none disabled:transform-none"
        >
          <!-- Hiệu ứng vệt sáng lướt qua khi trỏ chuột -->
          <div class="absolute inset-0 w-full h-full bg-gradient-to-r from-transparent via-white/30 to-transparent -translate-x-full group-hover:animate-[shimmer_1s_infinite]"></div>
          
          <span class="relative z-10 text-2xl">🚀</span>
          <span class="relative z-10 tracking-wide">{{ isLoading ? 'ĐANG PHÂN TÍCH...' : 'TIẾN HÀNH TẢI HÀNG LOẠT NGAY' }}</span>
        </button>
      </div>

      <!-- Box Kết quả tải -->
      <div v-if="results.length > 0 || isLoading" class="bg-white p-6 rounded-2xl shadow-sm border border-slate-200">
        <h3 class="text-lg font-bold text-slate-800 mb-4 border-b pb-2">Tiến trình xử lý:</h3>

        <div class="space-y-4">
          <!-- Item kết quả -->
          <div v-for="(item, index) in results" :key="index" class="flex items-center justify-between p-3 bg-slate-50 border border-slate-100 rounded-xl">
            <div class="truncate flex-1 mr-4">
              <p class="text-xs text-slate-500 truncate mb-1">{{ item.original_url }}</p>
              <p v-if="item.success" class="text-sm font-bold text-slate-800 truncate">{{ item.title || 'Video tải thành công' }}</p>
              <p v-else class="text-sm font-bold text-red-500">{{ item.error }}</p>
            </div>
            
            <!-- Sử dụng API force-download để ép tải MP4 xuống máy thay vì mở tab mới -->
            <div v-if="item.success" class="flex gap-2 shrink-0">
              <a 
                :href="`http://127.0.0.1:8000/api/v1/download/force-download?url=${encodeURIComponent(item.download_url)}&filename=FastVid_Bulk_${index + 1}.mp4`" 
                class="bg-green-500 hover:bg-green-600 text-white text-xs font-bold py-2 px-4 rounded-lg whitespace-nowrap transition-colors shadow-sm"
              >
                Tải MP4
              </a>
            </div>
          </div>

          <!-- Loading xoay tròn -->
          <div v-if="isLoading" class="flex flex-col items-center justify-center py-6">
            <svg class="animate-spin h-8 w-8 text-indigo-500 mb-2" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
              <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
              <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
            </svg>
            <p class="text-slate-500 font-medium text-sm">Đang kết nối tới máy chủ...</p>
          </div>
        </div>
      </div>
      
    </div>
  </div>
</template>

<style scoped>
/* Định nghĩa keyframe cho hiệu ứng vệt sáng lướt qua nút tải */
@keyframes shimmer {
  100% {
    transform: translateX(100%);
  }
}
</style>