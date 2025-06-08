<template>
  <div class="video-page landing">
    <video autoplay muted loop playsinline>
      <source src="/video/landing.mp4" type="video/mp4" />
      브라우저가 video 태그를 지원하지 않습니다.
    </video>
    <div class="overlay">
      <h1>Welcome to README</h1>
      <p>책과 사람을 연결하는 커뮤니티</p>
      <RouterLink :to="{ name: 'login' }" class="start-btn">지금 시작하기</RouterLink>

    </div>
  </div>
</template>

<script setup>
import { RouterLink } from 'vue-router'
</script>

<style scoped>
.video-page {
  position: relative;
  height: 100vh;
  overflow: hidden;
}
video {
  width: 100%;
  height: 100%;
  object-fit: cover;
}
.overlay {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  color: white;
  text-align: center;
  text-shadow: 1px 1px 4px rgba(0, 0, 0, 0.7);
}
.start-btn {
  display: inline-block;
  margin-top: 1rem;
  padding: 0.6rem 1.4rem;
  background: #6c63ff;
  color: white;
  border-radius: 30px;
  text-decoration: none;
  font-weight: 600;
}
</style>
