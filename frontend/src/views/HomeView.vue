<template>
  <section class="home-container">
    <!-- 1) 베스트셀러 캐러셀 -->
    <h2 class="section-title">베스트셀러</h2>
    <Splide v-if="bestsellers.length" :options="splideOptions">
      <SplideSlide v-for="book in bestsellers" :key="book.pk">
        <RouterLink :to="`/books/${book.id}`" class="carousel-card">
          <img :src="book.cover" alt="표지" />
          <p class="title">{{ book.title }}</p>
        </RouterLink>
      </SplideSlide>
    </Splide>

    <!-- 2) 평점 높은 책 캐러셀 -->
    <h2 class="section-title">유저 평점이 높은 책</h2>
    <Splide v-if="rankingBook.length" :options="splideOptions">
      <SplideSlide v-for="book in rankingBook" :key="book.pk">
        <RouterLink :to="`/books/${book.id}`" class="carousel-card">
          <img :src="book.cover" alt="표지" />
          <p class="title">{{ book.title }}</p>
        </RouterLink>
      </SplideSlide>
    </Splide>

    <!-- 3) 최신 쓰레드 + 더보기 -->
    <div class="section-title with-link">
      <h2>최신 포스트</h2>
      <RouterLink to="/threads" class="more-link">더보기 &gt;</RouterLink>
    </div>
    <ul class="thread-list">
      <li v-for="thr in latestThreads" :key="thr.pk" class="thread-card">
        <RouterLink :to="`/threads/${thr.id}`">
          <h3>{{ thr.title }}</h3>
          <p class="meta">{{ thr.user }} · {{ formatDate(thr.created_at) }}</p>
          <p class="excerpt">{{ thr.excerpt }}</p>
        </RouterLink>
      </li>
    </ul>
  </section>
</template>

<script setup>
import { ref, onMounted, nextTick } from 'vue'
import axios from 'axios'
import { Splide, SplideSlide } from '@splidejs/vue-splide'
import { RouterLink } from 'vue-router'
import { useBookStore } from '@/stores/book'

const bookStore = useBookStore()
const bestsellers = ref([])
const rankingBook = ref([])
const latestThreads = ref([])

const splideOptions = {
  type: 'loop',
  perPage: 4,
  perMove: 1,
  gap: '1rem',
  autoplay: true,
  pauseOnHover: true,
  pagination: true,
  trimSpace: false,
  start: 0,
  focus: 0,
  fixedWidth: '180px',
  focus: 'center',
}

function formatDate(dt) {
  return new Date(dt).toLocaleDateString('ko-KR', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit'
  })
}

async function fetchHomeData() {
  try {
    const { data } = await axios.get(`${bookStore.API_URL}/api/v1/home/`)
    bestsellers.value = data.bestsellers
    rankingBook.value = data.ranking_book
    latestThreads.value = data.latest_threads
  } catch (err) {
    console.error('홈 데이터 로드 실패:', err)
  }
}

onMounted(async () => {
  await fetchHomeData()
  await nextTick() // Splide 렌더링 안정화
})
</script>

<style scoped>
.home-container {
  padding: 2rem 1rem;
}

/* Splide 내부 커스터마이징 */
:deep(.splide__list) {
  justify-content: flex-start;
}

.section-title {
  font-size: 1.5rem;
  margin: 1.5rem 0 1rem;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.section-title.with-link {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.more-link {
  font-size: 0.9rem;
  color: #6c63ff;
  text-decoration: none;
  font-weight: 500;
}
.more-link:hover {
  text-decoration: underline;
}

.carousel-card {
  width: 160px;
  min-width: 160px;
  text-decoration: none;
  color: inherit;
  display: flex;
  flex-direction: column;
  align-items: center;
}
.carousel-card img {
  width: 100%;
  height: 230px;
  object-fit: cover;
  border-radius: 8px;
}
.carousel-card .title {
  margin-top: 0.5rem;
  font-size: 1rem;
  font-weight: 500;
}

.thread-list {
  list-style: none;
  padding: 0;
  margin: 0;
}
.thread-card {
  background: #fff;
  padding: 1rem;
  margin-bottom: 1rem;
  border-radius: 8px;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.05);
}
.thread-card h3 {
  margin: 0 0 0.5rem;
}
.thread-card .meta {
  font-size: 0.85rem;
  color: #666;
  margin-bottom: 0.5rem;
}
.thread-card .excerpt {
  font-size: 0.95rem;
  color: #333;
}
</style>
