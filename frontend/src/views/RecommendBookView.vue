<template>
  <div class="recommend-container">
    <h2>나에게 맞는 추천 도서</h2>

    <!-- 1. 관심 정보 없음 -->
    <div v-if="!hasInterest">
      <p>아직 관심 정보를 설정하지 않았어요.</p>
      <RouterLink :to="{ name: 'interestSetting' }">
        <button class="action-btn">관심 정보 설정하러 가기</button>
      </RouterLink>
    </div>

    <!-- 2. 관심 정보 있음 -->
    <div v-else>
      <!-- 2-1. 로딩 중 -->
      <div v-if="isLoading" class="loading-box">
        <p>추천 정보를 불러오는 중입니다...</p>
        <img src="/loading.gif" alt="로딩 중" width="50" />
      </div>

      <!-- 2-2. 추천 없음 -->
      <div v-else-if="!hasRecommendation">
        <p>아직 추천 기록이 없어요. 한 번 추천을 받아볼까요?</p>
        <button class="action-btn" @click="onGenerateRecommendation">추천 받기</button>
      </div>

      <!-- 2-3. 추천 있음 -->
      <div v-else>
        <button class="action-btn" @click="onGenerateRecommendation">다시 추천 받기</button>
        <ul class="book-list">
          <li v-for="(item, idx) in recommendations" :key="idx" class="book-item">
            
            <RouterLink
              :to="{ name: 'bookDetail', params: { bookId: item.id } }"
              class="book-link"
            >
              <img :src="item.cover || '/default-book.png'" alt="book cover" class="book-cover" />
              
              
              <h3 class="book-title">{{ item.title }}</h3>
              <p class="book-author"><strong>저자:</strong> {{ item.author }}</p>
            </RouterLink>
            <p class="similarity"><strong>유사한 이유:</strong> {{ item.similarity_reason }}</p>
            <p class="reason"><strong>추천 이유:</strong> {{ item.recommend_reason }}</p>
          </li>
        </ul>
      </div>
    </div>
  </div>
</template>

<script setup>
import { onMounted, computed, ref } from 'vue'
import { useAccountStore } from '@/stores/accounts'
import { useBookStore } from '@/stores/book'
import { storeToRefs } from 'pinia'

const accountStore = useAccountStore()
const bookStore = useBookStore()
const { recommendationStatus, recommendations } = storeToRefs(bookStore)

const API_URL = accountStore.API_URL

// 관심 정보 있는지 판단
const hasInterest = computed(() => {
  const user = accountStore.userInfo
  return (
    (user?.favorite_books?.length ?? 0) > 0 ||
    (user?.favorite_authors?.length ?? 0) > 0 ||
    (user?.favorite_topics?.length ?? 0) > 0
  )
})

// 추천 기다리는 중 
const isLoading = ref(false)

// 추천 결과 있는지 판단
const hasRecommendation = computed(() => {
  // console.log(recommendations.value)
  return Array.isArray(recommendations.value) && recommendations.value.length > 0
})

const onGenerateRecommendation = async () => {
  isLoading.value = true 
  await bookStore.createRecommendation()
  isLoading.value = false
}

onMounted(async () => {
  if (accountStore.currentUsername) {
    await accountStore.getUserInfo(accountStore.currentUsername)
  }

  if (accountStore.token) {
    await bookStore.fetchRecommendation(accountStore.token)
  }
})
</script>

<style scoped>
.recommend-container {
  max-width: 960px;
  margin: 4rem auto;
  padding: 2rem;
  font-family: 'Pretendard', sans-serif;
  text-align: center;
  animation: fadeIn 0.8s ease-in-out;
}

.action-btn {
  padding: 0.75rem 1.5rem;
  background-color: #6c63ff;
  color: white;
  border: none;
  border-radius: 30px;
  font-weight: 600;
  margin: 1rem 0;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.action-btn:hover {
  background-color: #584ff2;
}

.loading-box {
  margin: 2rem 0;
  color: #666;
}

.book-list {
  list-style: none;
  padding: 0;
  display: flex;
  flex-wrap: wrap;
  gap: 2rem;
  justify-content: center;
  margin-top: 2rem;
}

.book-item {
  width: 220px;
  background-color: #fff;
  border-radius: 16px;
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.06);
  padding: 1.2rem;
  transition: transform 0.3s ease;
  text-align: left;
}

.book-item:hover {
  transform: translateY(-5px);
}

.book-link {
  text-decoration: none;
  color: inherit;
}

.book-cover {
  width: 100%;
  height: 150px;
  object-fit: cover;
  border-radius: 12px;
  margin-bottom: 1rem;
}

.book-title {
  font-size: 1.1rem;
  font-weight: 600;
  color: #1a1a1a;
}

.book-author {
  font-size: 0.95rem;
  color: #555;
  margin-bottom: 0.5rem;
}

.similarity, .reason {
  font-size: 0.9rem;
  color: #444;
  margin-top: 0.4rem;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
</style>
