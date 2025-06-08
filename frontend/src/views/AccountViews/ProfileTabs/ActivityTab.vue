<template>
  <div class="activity-container">
    <h3>스크랩한 책</h3>

    <div v-if="likedBooks.length === 0" class="empty-message">
      아직 스크랩한 책이 없어요!
    </div>

    <div class="book-list" v-else>
      <div
        v-for="book in likedBooks"
        :key="book.id"
        class="book-card"
        @click="$router.push({ name: 'bookDetail', params: { bookId: book.id } })"
      >
        <img :src="book.cover" alt="책 표지" class="book-cover" />
        <div class="book-info">
          <h4>{{ book.title }}</h4>
          <p>{{ book.author }}</p>
        </div>
      </div>
    </div>

    <h3>좋아요한 포스트</h3>

    <div v-if="likedThreads.length === 0" class="empty-message">
      아직 좋아요한 포스트 없어요!
    </div>

    <ul class="thread-list" v-else>
      <li
        v-for="thread in likedThreads"
        :key="thread.id"
        class="thread-card"
        @click="$router.push(`/threads/${thread.id}`)"
      >
        <h4 class="thread-title">{{ thread.title }}</h4>
        <p class="thread-author">작성자: {{ thread.user.username }}</p>
        <p class="thread-date">📅 {{ formatDate(thread.created_at) }}</p>
      </li>
    </ul>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useAccountStore } from '@/stores/accounts'

const accountStore = useAccountStore()

const likedBooks = computed(() => {
  return Array.isArray(accountStore.userInfo?.liked_books)
    ? accountStore.userInfo.liked_books
    : []
})

const likedThreads = computed(() => {
  return Array.isArray(accountStore.userInfo?.liked_threads)
    ? accountStore.userInfo.liked_threads
    : []
})

const formatDate = (dateStr) => {
  const date = new Date(dateStr)
  return date.toLocaleDateString('ko-KR', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
  })
}
</script>

<style scoped>
.activity-container {
  max-width: 960px;
  margin: 3rem auto;
  padding: 1rem;
  font-family: 'Pretendard', sans-serif;
}

h3 {
  font-size: 1.5rem;
  margin: 2rem 0 1rem;
}

.empty-message {
  text-align: center;
  color: #888;
  margin-top: 1rem;
}

/* 좋아요한 책 카드 */
.book-list {
  display: flex;
  flex-wrap: wrap;
  gap: 1.5rem;
  justify-content: flex-start;
}
.book-card {
  width: 200px;
  padding: 1rem;
  border: 1px solid #ddd;
  border-radius: 12px;
  background-color: #fff;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.05);
  cursor: pointer;
  transition: transform 0.3s ease;
  text-align: left;
}
.book-card:hover {
  transform: translateY(-5px);
}
.book-cover {
  width: 100%;
  height: 160px;
  object-fit: cover;
  border-radius: 8px;
  margin-bottom: 0.5rem;
}
.book-info h4 {
  margin: 0;
  font-size: 1rem;
  font-weight: 600;
  color: #222;
}
.book-info p {
  margin: 0.3rem 0 0;
  font-size: 0.9rem;
  color: #666;
}

/* 좋아요한 쓰레드 카드 */
.thread-list {
  list-style: none;
  padding: 0;
  display: grid;
  grid-template-columns: 1fr;
  gap: 1.5rem;
}

.thread-card {
  padding: 1rem 1.5rem;
  border: 1px solid #ddd;
  border-radius: 12px;
  background-color: #fff;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
  cursor: pointer;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}
.thread-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 6px 16px rgba(0, 0, 0, 0.08);
}

.thread-title {
  margin: 0;
  font-size: 1.1rem;
  font-weight: 600;
  color: #222;
}

.thread-author,
.thread-date {
  font-size: 0.9rem;
  color: #666;
  margin-top: 0.4rem;
}
</style>
