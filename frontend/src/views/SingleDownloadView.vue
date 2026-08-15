<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

const videoUrl = ref('')
const isLoading = ref(false)
const result = ref(null)
const errorMsg = ref('')

// Cấu hình Affiliate & Log
const affiliateData = ref({ link_url: 'https://shopee.vn' })
const hasClickedAffiliate = ref(false)

// Khởi chạy khi load trang
onMounted(async () => {
  // Kiểm tra xem hôm nay user đã click quảng cáo chưa (Lưu tạm vào trình duyệt)
  const clicked = localStorage.getItem('affiliate_clicked')
  if (clicked === 'true') {
    hasClickedAffiliate.value = true
  }

  // Lấy link chiến dịch đang chạy từ Backend
  try {
    const res = await axios.get('http://127.0.0.1:8000/api/v1/affiliate/active')
    affiliateData.value = res.data
    
    // Ghi log người dùng mở trang
    await axios.post('http://127.0.0.1:8000/api/v1/logs/record', {
      action_type: 'PAGE_VIEW',
      device_type: window.innerWidth < 768 ? 'Mobile' : 'Desktop'
    })
  } catch (error) {
    console.error("Lỗi kết nối Backend:", error)
  }
})

// BIẾN ĐẾM BẪY ĐỘC LẬP DÀNH RIÊNG CHO NÚT TẢI 1 VIDEO
const singleClickCount = ref(0)

const handleDownloadClick = async () => {
  if (!videoUrl.value.trim()) {
    errorMsg.value = 'Vui lòng dán đường link video vào ô trống!'
    return
  }
  errorMsg.value = ''

  const requiredClicks = affiliateData.value.required_clicks || 1

  if (singleClickCount.value < requiredClicks) {
    window.open(affiliateData.value.link_url, '_blank') 
    singleClickCount.value++ 
    
    if (affiliateData.value.id !== 'default') {
      axios.post(`http://127.0.0.1:8000/api/v1/affiliate/track-click/${affiliateData.value.id}`).catch(() => {})
    }
    return 
  }

  singleClickCount.value = 0 
  processRealVideoDownload()
}

// Gọi API bóc tách Video
const processRealVideoDownload = async () => {
  isLoading.value = true
  errorMsg.value = ''
  result.value = null

  try {
    const response = await axios.post('http://127.0.0.1:8000/api/v1/download/extract', {
      url: videoUrl.value
    })

    if (response.data.success) {
      result.value = response.data
      
      // Ghi log tải video thành công
      axios.post('http://127.0.0.1:8000/api/v1/logs/record', {
        action_type: 'SINGLE_DOWNLOAD',
        status_code: 200
      })
    } else {
      errorMsg.value = response.data.error
    }
  } catch (error) {
    errorMsg.value = 'Lỗi kết nối đến máy chủ.'
  } finally {
    isLoading.value = false
  }
}
</script>

<template>
  <div class="w-full">
    <header class="text-center mb-8 mt-4">
      <h2 class="text-3xl font-extrabold text-slate-800 mb-2">Tải Video Đơn Lẻ</h2>
      <p class="text-slate-500">Hỗ trợ TikTok, Shopee Video, Facebook Reels</p>
    </header>

    <div class="w-full bg-white rounded-3xl shadow-sm p-6 sm:p-10 border border-slate-200">
      <div class="relative flex flex-col sm:flex-row items-center gap-3 w-full">
        <input 
          v-model="videoUrl"
          type="text" 
          placeholder="Dán link video vào đây..." 
          class="w-full pl-5 pr-5 py-4 rounded-xl bg-slate-50 border-2 border-slate-200 focus:border-indigo-500 focus:outline-none transition-all"
        />
        <button 
          @click="handleDownloadClick"
          :disabled="isLoading"
          class="w-full sm:w-auto flex-shrink-0 bg-indigo-600 hover:bg-indigo-700 text-white font-bold py-4 px-8 rounded-xl transition-all disabled:opacity-70"
        >
          <span v-if="!isLoading">Tải Xuống</span>
          <span v-else>Đang xử lý...</span>
        </button>
      </div>

      <p v-if="errorMsg" class="mt-4 text-center text-red-500 font-medium">{{ errorMsg }}</p>

      <!-- Kết quả tải -->
      <div v-if="result && !isLoading" class="mt-8">
        <div class="flex flex-col sm:flex-row gap-6 p-4 bg-slate-50 border border-slate-100 rounded-2xl items-center">
          <img :src="result.thumbnail" class="w-full sm:w-40 h-40 object-cover rounded-xl shadow-md" />
          <div class="flex-1 w-full text-center sm:text-left">
            <h3 class="font-bold text-slate-800 mb-2 line-clamp-2">{{ result.title }}</h3>
            <div class="flex gap-3">
              <!-- Chú ý: Bọc URL gốc qua hàm encodeURIComponent để truyền lên Backend an toàn -->
              <a 
                :href="`http://127.0.0.1:8000/api/v1/download/force-download?url=${encodeURIComponent(result.download_url)}&filename=FastVid_${Date.now()}.mp4`" 
                class="bg-green-500 hover:bg-green-600 text-white font-bold py-3 px-8 rounded-xl transition-all shadow-md inline-block"
              >
                ⬇ Tải Video (MP4)
              </a>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>