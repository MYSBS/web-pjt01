
// src/views/Error500.vue
<template>
  <div class="error-page">
    <h1>500 - 서버 오류</h1>
    <p>문제가 발생했습니다. 아래 내용을 참고해주세요:</p>
    <pre v-if="message">{{ message }}</pre>
    <button @click="goHome">홈으로 이동</button>
  </div>
</template>

<script setup>
import { defineProps } from 'vue'
import { useRouter } from 'vue-router'

const props = defineProps({
  message: {
    type: String,
    default: ''
  }
})

const router = useRouter()

function goHome() {
  router.push({ name: 'main' })
}
</script>

<style scoped>
.error-page {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 80vh;
  text-align: center;
}
.error-page h1 {
  font-size: 2rem;
  margin-bottom: 1rem;
}
.error-page pre {
  background: #f5f5f5;
  padding: 1rem;
  border-radius: 4px;
  max-width: 80%;
  overflow-x: auto;
  margin-bottom: 1rem;
}
.error-page button {
  padding: 0.5rem 1rem;
  border: none;
  background-color: #ff6b6b;
  color: white;
  border-radius: 4px;
  cursor: pointer;
}
.error-page button:hover {
  background-color: #e05656;
}
</style>
