// src/views/Error404.vue
<template>
  <div class="error-page">
    <h1>404 - 페이지를 찾을 수 없습니다</h1>
    <p>죄송합니다. 요청하신 페이지는 존재하지 않습니다:</p>
    <code>{{ route.fullPath }}</code>
    <button @click="goHome">홈으로 이동</button>
  </div>
</template>

<script setup>
import { useRouter, useRoute } from 'vue-router'

const router = useRouter()
const route = useRoute()

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
.error-page code {
  display: block;
  margin: 1rem 0;
  background: #f5f5f5;
  padding: 0.5rem;
  border-radius: 4px;
}
.error-page button {
  padding: 0.5rem 1rem;
  border: none;
  background-color: #42b983;
  color: white;
  border-radius: 4px;
  cursor: pointer;
}
.error-page button:hover {
  background-color: #369f6b;
}
</style>

