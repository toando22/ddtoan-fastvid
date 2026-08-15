import { createApp } from 'vue'
import './style.css' 
import App from './App.vue'
import router from './router/index.js' 
import axios from 'axios'

// --- THUẬT TOÁN ĐÁNH CHẶN (INTERCEPTOR) TỰ ĐỘNG ---
// Tự động dò tìm và cắt bỏ domain localhost ở mọi file component.
// Trình duyệt sẽ tự động gọi API bằng domain hiện tại (fastvid.click) gửi tới Nginx.
axios.interceptors.request.use((config) => {
  if (config.url && config.url.includes('http://127.0.0.1:8000')) {
    config.url = config.url.replace('http://127.0.0.1:8000', '');
  }
  return config;
});

createApp(App).use(router).mount('#app')