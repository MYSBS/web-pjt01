// 1. 전역 스타일·라이브러리 CSS import
import 'bootstrap/dist/css/bootstrap.min.css'
import '@splidejs/splide/dist/css/splide.min.css'
import 'leaflet/dist/leaflet.css'
import '@/assets/main.css'

// 2. 전역 라이브러리 JS import
import 'bootstrap/dist/js/bootstrap.bundle.min.js'

// 3. Vue 앱 생성 및 플러그인·컴포넌트 import
import { createApp } from 'vue'
import { createPinia } from 'pinia'
import piniaPluginPersistedstate from 'pinia-plugin-persistedstate'
import { Splide, SplideSlide } from '@splidejs/vue-splide'

import App from './App.vue'
import router from './router'

// 4. 앱 인스턴스 생성
const app = createApp(App)

// 5. Pinia 세팅 (persistedstate 플러그인 포함)
const pinia = createPinia()
pinia.use(piniaPluginPersistedstate)
app.use(pinia)

// 6. Vue Router
app.use(router)

// 7. 전역 컴포넌트 등록
app.component('Splide', Splide)
app.component('SplideSlide', SplideSlide)

// 8. 마운트
app.mount('#app')
