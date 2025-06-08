<template>
  <section class="threads-grid-container">
    <h1 class="threads-title">전체 글 목록</h1>
    <div class="thread-grid">
      <div
        v-for="thread in reversedThreads"
        :key="thread.id"
        class="thread-card"
      >
        <RouterLink
          :to="{ name: 'threadDetail', params: { threadId: thread.id } }"
          class="thread-link"
        >
          <img
            :src="
              thread.cover_img
                ? (thread.cover_img.startsWith('http')
                    ? thread.cover_img
                    : `${bookStore.API_URL}${thread.cover_img}`)
                : defaultImg
            "
            alt="표지"
            class="thread-image"
          />
          <div class="thread-info">
            <h3>{{ thread.title }}</h3>
            <p>{{ new Date(thread.created_at).toLocaleDateString('ko-KR') }}</p>
          </div>
        </RouterLink>
      </div>
    </div>
  </section>
</template>

<script setup>
import defaultImg from '@/assets/images/defaultimg.png'
import { computed, onMounted } from 'vue'
import { RouterLink } from 'vue-router'
import { useThreadStore } from '@/stores/threads'
import { useBookStore } from '@/stores/book'

const threadStore = useThreadStore()
const bookStore = useBookStore()

onMounted(() => {
  threadStore.getThreads()
})

const reversedThreads = computed(() =>
  [...threadStore.threadList].reverse()
)
</script>

<style scoped>
.threads-grid-container {
  max-width: 1100px;
  margin: 5rem auto;
  padding: 2rem;
  background-color: #f8f8f8;
  font-family: 'Pretendard', 'Helvetica Neue', sans-serif;
}

.threads-title {
  font-size: 2.4rem;
  text-align: center;
  margin-bottom: 3rem;
  font-weight: 600;
  color: #1a1a1a;
}

.thread-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 1.5rem;
}

.thread-card {
  background-color: #ffffff;
  border-radius: 1rem;
  overflow: hidden;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  box-shadow: 0 6px 16px rgba(0, 0, 0, 0.05);
  border: 1px solid #eaeaea;
}

.thread-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 10px 24px rgba(0, 0, 0, 0.08);
}

.thread-link {
  display: flex;
  flex-direction: column;
  text-decoration: none;
  color: inherit;
}

.thread-image {
  width: 100%;
  aspect-ratio: 1 / 1;
  object-fit: cover;
  border-bottom: 1px solid #eee;
}

.thread-info {
  padding: 1rem;
  display: flex;
  flex-direction: column;
  gap: 0.3rem;
}

.thread-info h3 {
  font-size: 1rem;
  font-weight: 600;
  color: #1a1a1a;
  margin: 0;
}

.thread-info p {
  font-size: 0.85rem;
  color: #555;
  margin: 0;
}
</style>
