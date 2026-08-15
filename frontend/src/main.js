import { createApp } from 'vue'
import './style.css' // Đã sửa đường dẫn CSS
import App from './App.vue'
import router from './router/index.js' // Đường dẫn này sẽ đúng sau khi bạn kéo thư mục router vào src

createApp(App).use(router).mount('#app')