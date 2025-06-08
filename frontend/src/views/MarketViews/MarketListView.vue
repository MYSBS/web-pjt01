<template>
  <div class="market-container">
    <div class="market-header">
      <h2 class="market-title">중고거래 마켓</h2>
      <RouterLink :to="{ name: 'MarketCreateView' }" class="btn btn-market">
        + 게시글 작성하기
      </RouterLink>
    </div>

    <!-- 검색창 -->
    <div class="search-bar">
      <input
        v-model="searchQuery"
        type="text"
        placeholder="제목, 내용, 책 제목 또는 저자를 입력하세요"
        class="search-input"
      />
    </div>

    <!-- 게시글 리스트 -->
    <div v-if="filteredPosts.length" class="market-list">
      <RouterLink
        v-for="post in paginatedPosts"
        :key="post.id"
        :to="{ name: 'MarketDetailView', params: { marketId: post.id } }"
        class="market-item"
      >
        <div class="market-card">
          <img :src="post.book.cover" alt="책 표지" class="cover-img" />
          <div class="market-info">
            <h4 class="market-title-text">{{ post.title }}</h4>
            <p><strong>작성자:</strong> {{ post.user.username }}</p>
            <p><strong>가격:</strong> {{ post.price ? post.price + '₩' : '미기재' }}</p>
            <p><strong>책:</strong> {{ post.book.title }} / {{ post.book.author }}</p>
            <p><strong>작성일:</strong> {{ formatDate(post.created_at) }}</p>
            <div class="icons">
              <span>❤️ {{ post.likes_count }}</span>
              <span>💬 {{ post.comments_count }}</span>
            </div>
          </div>
        </div>
      </RouterLink>

      <!-- 페이지네이션 -->
      <div class="pagination">
        <button class="page-btn" :disabled="currentPage === 1" @click="goToPage(currentPage - 1)">&lt;</button>
        <button
          v-for="page in totalPages"
          :key="page"
          :class="['page-btn', { active: currentPage === page }]"
          @click="goToPage(page)"
        >
          {{ page }}
        </button>
        <button class="page-btn" :disabled="currentPage === totalPages" @click="goToPage(currentPage + 1)">&gt;</button>
      </div>
    </div>

    <div v-else class="empty-message">검색 결과가 없습니다.</div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useMarketStore } from '@/stores/markets'

const marketStore = useMarketStore()
const searchQuery = ref('')
const currentPage = ref(1)
const itemsPerPage = 10

onMounted(() => {
  marketStore.fetchMarketPosts()
})

const filteredPosts = computed(() => {
  return marketStore.marketPosts.filter(post => {
    const keyword = searchQuery.value.toLowerCase()
    return (
      post.title.toLowerCase().includes(keyword) ||
      post.content.toLowerCase().includes(keyword) ||
      post.book.title.toLowerCase().includes(keyword) ||
      post.book.author.toLowerCase().includes(keyword)
    )
  })
})

const paginatedPosts = computed(() => {
  const start = (currentPage.value - 1) * itemsPerPage
  return filteredPosts.value.slice(start, start + itemsPerPage)
})

const totalPages = computed(() => Math.ceil(filteredPosts.value.length / itemsPerPage))

const goToPage = (page) => {
  currentPage.value = page
}

const formatDate = (dateStr) => {
  const date = new Date(dateStr)
  return `${date.getFullYear()}. ${date.getMonth() + 1}. ${date.getDate()}.`
}
</script>

<style scoped>
.market-container {
  max-width: 960px;
  margin: 0 auto;
  padding: 2rem 1rem;
  background-color: #f9f9f9;
  font-family: 'Pretendard', sans-serif;
}

.market-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
}

.market-title {
  font-size: 2rem;
  font-weight: bold;
  color: #1a1a1a;
}

.btn-market {
  background-color: #6c63ff;
  color: white;
  padding: 0.5rem 1rem;
  border-radius: 8px;
  font-weight: 600;
}

.search-bar {
  margin-bottom: 2rem;
  text-align: center;
}

.search-input {
  width: 100%;
  max-width: 480px;
  padding: 0.6rem 1rem;
  border: 1px solid #ccc;
  border-radius: 8px;
  font-size: 1rem;
}

.market-list {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.market-item {
  text-decoration: none;
  color: inherit;
}

/* ✅ 책커버 왼쪽, 정보 오른쪽, 높이 맞춤 */
.market-card {
  display: grid;
  grid-template-columns: auto 1fr;
  align-items: stretch;
  gap: 1.5rem;
  background-color: white;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
  padding: 1rem;
}

.cover-img {
  width: 100px;
  height: auto;
  max-height: 180px;
  object-fit: cover;
  border-radius: 6px;
  align-self: stretch;
}

.market-info {
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  flex-grow: 1;
}

.market-title-text {
  font-size: 1.2rem;
  font-weight: 600;
  margin-bottom: 0.3rem;
}

.market-info p {
  margin: 0.3rem 0;
  color: #333;
  font-size: 0.95rem;
}

.icons {
  margin-top: 0.5rem;
  color: #888;
  font-size: 0.9rem;
  display: flex;
  gap: 1rem;
}

.empty-message {
  text-align: center;
  margin-top: 4rem;
  color: #888;
  font-size: 1rem;
}

.pagination {
  display: flex;
  justify-content: center;
  gap: 0.5rem;
  margin-top: 2rem;
  flex-wrap: wrap;
}

.page-btn {
  background-color: transparent;
  color: #6c63ff;
  border: 1px solid #6c63ff;
  padding: 0.4rem 0.8rem;
  border-radius: 20px;
  font-weight: 600;
  cursor: pointer;
}

.page-btn.active,
.page-btn:hover {
  background-color: #6c63ff;
  color: white;
}

/* ✅ 반응형 */
@media (max-width: 768px) {
  .market-card {
    grid-template-columns: 1fr;
    grid-template-rows: auto auto;
    text-align: center;
  }

  .cover-img {
    width: 80px;
    height: 110px;
    margin: 0 auto;
  }

  .market-info {
    margin-top: 1rem;
    align-items: center;
  }
}
</style>
