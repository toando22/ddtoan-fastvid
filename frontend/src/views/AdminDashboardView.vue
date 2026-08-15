<script setup>
import { ref, onMounted, computed } from 'vue'
import axios from 'axios'

const affiliates = ref([])
const newCampaign = ref({ campaign_name: '', link_url: '', priority: 0, required_clicks: 1, is_active: true })
const isSubmitting = ref(false)

// State cho Popup Edit
const showEditModal = ref(false)
const editData = ref({})

const fetchAffiliates = async () => {
  try {
    const res = await axios.get('http://127.0.0.1:8000/api/v1/affiliate/all')
    affiliates.value = res.data
  } catch (error) {
    console.error("Lỗi lấy dữ liệu:", error)
  }
}

onMounted(() => { fetchAffiliates() })

// TÍNH TOÁN KPI THỐNG KÊ
const totalClicks = computed(() => affiliates.value.reduce((sum, item) => sum + (item.click_count || 0), 0))
const activeCount = computed(() => affiliates.value.filter(item => item.is_active).length)
const topCampaign = computed(() => {
  if (affiliates.value.length === 0) return 'Chưa có'
  const top = [...affiliates.value].sort((a, b) => (b.click_count || 0) - (a.click_count || 0))[0]
  return top.campaign_name
})

const handleAddAffiliate = async () => {
  if (!newCampaign.value.campaign_name || !newCampaign.value.link_url) return alert("Nhập đủ Tên và Link!")
  isSubmitting.value = true
  try {
    const res = await axios.post('http://127.0.0.1:8000/api/v1/affiliate/add', newCampaign.value)
    if (res.data.success) {
      newCampaign.value = { campaign_name: '', link_url: '', priority: 0, required_clicks: 1, is_active: true }
      fetchAffiliates()
    }
  } finally { isSubmitting.value = false }
}

const toggleStatus = async (id) => {
  const res = await axios.put(`http://127.0.0.1:8000/api/v1/affiliate/toggle/${id}`)
  if (res.data.success) fetchAffiliates()
}

// XỬ LÝ SỬA CHIẾN DỊCH
const openEditModal = (item) => {
  editData.value = { ...item } // Clone data ra để sửa không ảnh hưởng trực tiếp tới view
  showEditModal.value = true
}

const handleSaveEdit = async () => {
  try {
    const res = await axios.put(`http://127.0.0.1:8000/api/v1/affiliate/edit/${editData.value.id}`, editData.value)
    if (res.data.success) {
      showEditModal.value = false
      fetchAffiliates() // Load lại bảng
    }
  } catch (error) {
    alert("Lỗi khi lưu chỉnh sửa.")
  }
}
</script>

<template>
  <div class="w-full max-w-6xl mx-auto relative">
    
    <header class="mb-6 mt-4">
      <h2 class="text-3xl font-extrabold text-slate-800 mb-2">Admin Dashboard</h2>
      <p class="text-slate-500">Thống kê & Điều hướng chiến dịch bẫy link</p>
    </header>

    <!-- KHU VỰC THẺ THỐNG KÊ (KPI) -->
    <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
      <div class="bg-white p-6 rounded-2xl shadow-sm border border-slate-200 flex items-center gap-4">
        <div class="w-12 h-12 bg-indigo-100 rounded-full flex items-center justify-center text-indigo-600 font-bold text-xl">🚀</div>
        <div>
          <p class="text-sm font-semibold text-slate-500">Đang hoạt động</p>
          <p class="text-2xl font-black text-slate-800">{{ activeCount }} <span class="text-sm font-medium text-slate-500">chiến dịch</span></p>
        </div>
      </div>
      <div class="bg-white p-6 rounded-2xl shadow-sm border border-slate-200 flex items-center gap-4">
        <div class="w-12 h-12 bg-orange-100 rounded-full flex items-center justify-center text-orange-600 font-bold text-xl">🖱️</div>
        <div>
          <p class="text-sm font-semibold text-slate-500">Tổng thu hoạch Click</p>
          <p class="text-2xl font-black text-slate-800">{{ totalClicks }} <span class="text-sm font-medium text-slate-500">lượt dính bẫy</span></p>
        </div>
      </div>
      <div class="bg-white p-6 rounded-2xl shadow-sm border border-slate-200 flex items-center gap-4">
        <div class="w-12 h-12 bg-green-100 rounded-full flex items-center justify-center text-green-600 font-bold text-xl">👑</div>
        <div class="flex-1 min-w-0">
          <p class="text-sm font-semibold text-slate-500">Top Chiến dịch</p>
          <p class="text-lg font-black text-slate-800 truncate">{{ topCampaign }}</p>
        </div>
      </div>
    </div>

    <!-- KHU VỰC QUẢN LÝ -->
    <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
      
      <!-- FORM THÊM LINK MỚI -->
      <div class="lg:col-span-1 bg-white rounded-2xl shadow-sm border border-slate-200 p-6 self-start sticky top-20">
        <h3 class="text-lg font-bold text-slate-800 mb-4 border-b pb-2">➕ Gắn Link Mới</h3>
        <div class="space-y-4">
          <div><label class="block text-sm font-semibold text-slate-700 mb-1">Tên Chiến Dịch</label>
          <input v-model="newCampaign.campaign_name" type="text" class="w-full px-3 py-2 border rounded-lg focus:border-indigo-500 outline-none text-sm" /></div>
          <div><label class="block text-sm font-semibold text-slate-700 mb-1">Đường Link</label>
          <input v-model="newCampaign.link_url" type="text" class="w-full px-3 py-2 border rounded-lg focus:border-indigo-500 outline-none text-sm" /></div>
          <div class="flex gap-4">
            <div class="flex-1"><label class="block text-sm font-semibold text-slate-700 mb-1">Độ Ưu Tiên</label>
            <input v-model="newCampaign.priority" type="number" class="w-full px-3 py-2 border rounded-lg focus:border-indigo-500 outline-none text-sm" /></div>
            <div class="flex-1"><label class="block text-sm font-semibold text-slate-700 mb-1 text-red-600">Số Lần Bẫy</label>
            <input v-model="newCampaign.required_clicks" type="number" min="1" class="w-full px-3 py-2 border border-red-300 bg-red-50 rounded-lg outline-none text-sm font-bold text-center" /></div>
          </div>
          <button @click="handleAddAffiliate" :disabled="isSubmitting" class="w-full bg-indigo-600 hover:bg-indigo-700 text-white font-bold py-3 rounded-xl transition-all shadow-md mt-2">Thêm Mới</button>
        </div>
      </div>

      <!-- BẢNG DANH SÁCH -->
      <div class="lg:col-span-2 bg-white rounded-2xl shadow-sm border border-slate-200 p-6 overflow-x-auto">
        <h3 class="text-lg font-bold text-slate-800 mb-4 border-b pb-2">📋 Quản lý Link</h3>
        <table class="w-full text-left border-collapse">
          <thead>
            <tr class="bg-slate-50 text-slate-500 text-xs uppercase tracking-wider">
              <th class="p-3 font-semibold">Chiến dịch</th>
              <th class="p-3 font-semibold text-center">Bẫy</th>
              <th class="p-3 font-semibold text-center">Ưu tiên</th>
              <th class="p-3 font-semibold text-center">Click</th>
              <th class="p-3 font-semibold text-center">Thao tác</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-slate-100">
            <tr v-for="item in affiliates" :key="item.id" class="hover:bg-slate-50">
              <td class="p-3">
                <p class="font-bold text-slate-800 text-sm mb-1">{{ item.campaign_name }}</p>
                <a :href="item.link_url" target="_blank" class="text-xs text-indigo-500 hover:underline truncate max-w-[150px] block">{{ item.link_url }}</a>
              </td>
              <td class="p-3 text-center font-bold text-red-500">{{ item.required_clicks }}</td>
              <td class="p-3 text-center font-medium">{{ item.priority }}</td>
              <td class="p-3 text-center"><span class="bg-orange-100 text-orange-600 py-1 px-3 rounded-full text-xs font-bold">{{ item.click_count }}</span></td>
              <td class="p-3 flex justify-center gap-2 items-center">
                <!-- Nút Tắt/Bật -->
                <button @click="toggleStatus(item.id)" :class="item.is_active ? 'bg-green-500 hover:bg-green-600' : 'bg-slate-300 hover:bg-slate-400 text-slate-600'" class="text-white text-xs font-bold py-1.5 px-3 rounded-lg w-20 transition-colors">
                  {{ item.is_active ? 'Bật' : 'Tắt' }}
                </button>
                <!-- Nút Sửa -->
                <button @click="openEditModal(item)" class="bg-blue-100 hover:bg-blue-200 text-blue-600 py-1.5 px-2.5 rounded-lg transition-colors">
                  ✏️
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- POPUP SỬA (Hiển thị khi bấm nút ✏️) -->
    <div v-if="showEditModal" class="fixed inset-0 bg-slate-900/50 flex justify-center items-center z-50 animate-fade-in">
      <div class="bg-white w-full max-w-md rounded-2xl p-6 shadow-2xl relative">
        <button @click="showEditModal = false" class="absolute top-4 right-4 text-slate-400 hover:text-slate-600 font-bold text-xl">&times;</button>
        <h3 class="text-xl font-black text-slate-800 mb-6">✏️ Chỉnh sửa Chiến dịch</h3>
        
        <div class="space-y-4">
          <div><label class="block text-sm font-semibold text-slate-700 mb-1">Tên Chiến Dịch</label>
          <input v-model="editData.campaign_name" type="text" class="w-full px-3 py-2 border rounded-lg focus:border-indigo-500 outline-none" /></div>
          <div><label class="block text-sm font-semibold text-slate-700 mb-1">Đường Link</label>
          <input v-model="editData.link_url" type="text" class="w-full px-3 py-2 border rounded-lg focus:border-indigo-500 outline-none" /></div>
          
          <div class="flex gap-4">
            <div class="flex-1"><label class="block text-sm font-semibold text-slate-700 mb-1 text-red-600">Số lần Bẫy</label>
            <input v-model="editData.required_clicks" type="number" class="w-full px-3 py-2 border border-red-300 bg-red-50 rounded-lg font-bold text-center" /></div>
            
            <div class="flex-1"><label class="block text-sm font-semibold text-slate-700 mb-1">Sửa Lượt Click</label>
            <input v-model="editData.click_count" type="number" class="w-full px-3 py-2 border bg-orange-50 border-orange-200 rounded-lg font-bold text-center text-orange-600" /></div>
          </div>
          
          <button @click="handleSaveEdit" class="w-full bg-blue-600 hover:bg-blue-700 text-white font-bold py-3 rounded-xl transition-all shadow-md mt-4">
            Cập Nhật Lập Tức
          </button>
        </div>
      </div>
    </div>

  </div>
</template>