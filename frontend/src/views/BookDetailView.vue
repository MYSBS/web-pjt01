<template>
  <div v-if="book" class="book-detail-view">
    <!-- 헤더 -->
    <header class="book-header">
      <h1 class="book-title">{{ book.title }}</h1>
      <div class="book-header-actions">
        <RouterLink
          :to="{ name: 'thread-write', params: { bookId: book.id } }"
          class="thread-button"
        >
          📌 Post 작성
        </RouterLink>
        <button
          class="like-button"
          :class="{ liked: isLiked }"
          @click="onToggleLike"
        >
          {{ isLiked ? "💔 스크랩 취소" : "❤️ 스크랩" }}
          <span>({{ likeCount }})</span>
        </button>
      </div>
    </header>

    <!-- 책 상세 정보 -->
    <section class="book-detail-wrapper">
      <img :src="book.cover" class="book-cover" alt="책 표지" />
      <div class="book-text">
        <p class="book-description">{{ book.description }}</p>
        <div class="book-meta">
          <p><strong>부제:</strong> {{ book.subTitle }}</p>
          <p><strong>출판사:</strong> {{ book.publisher }}</p>
          <p><strong>출판일:</strong> {{ book.pub_date }}</p>
          <p><strong>ISBN:</strong> {{ book.isbn }}</p>
          <p><strong>평점:</strong> {{ book.customer_review_rank }}</p>
        </div>
      </div>
    </section>

    <!-- 별점 -->
    <StarRating :bookId="book.id" />
    <!-- 추천 책 -->
     <h2 class="author-title"> 
      <svg width="36" height="36" viewBox="0 0 36 36" fill="none" xmlns="http://www.w3.org/2000/svg">
        <circle cx="18" cy="18" r="16" fill="#E3F2FD" stroke="#1976D2" stroke-width="2"/>
        <path d="M12 18c0-3.31 2.69-6 6-6s6 2.69 6 6-2.69 6-6 6" fill="#BBDEFB"/>
        <path d="M18 12v2M18 22v2M12 18h2M22 18h2M15.5 15.5l1.2 1.2M20.5 20.5l1.2 1.2M20.5 15.5l-1.2 1.2M15.5 20.5l-1.2 1.2" stroke="#1976D2" stroke-width="1.5" stroke-linecap="round"/>
        <polygon points="28,10 29,13 32,13 29.5,15 30.5,18 28,16.5 25.5,18 26.5,15 24,13 27,13" fill="#FFD600" stroke="#FFA000" stroke-width="1"/>
      </svg>

      [AI] 추천 연관 도서
    </h2>
    <div class="recommendation-cards">
      <div v-for="rec in recommendations" :key="rec.id" class="card" @click="onMove(rec.id)">
        <h3 class="card-title">{{ rec.title }}</h3>
        <img :src="rec.cover" alt="커버이미지" class="card-image" />
        <p class="card-keywords">키워드: {{ rec.keywords.join(", ") }}</p>
      </div>
    </div>

    <!-- 작가 정보 -->
    <h2 class="author-title">👤 작가 정보</h2>
    <div class="author-section">
      <img :src="book.author_photo" class="author-photo" alt="작가 사진" />
      <div class="author-text">
        <h3>{{ book.author }}</h3>
        <p>{{ book.author_info }}</p>
      </div>
    </div>

    <!-- 지도 -->
    <h2 class="author-title">
      <svg width="64" height="64" viewBox="0 0 64 64" fill="none" xmlns="http://www.w3.org/2000/svg">
        <rect x="8" y="10" width="48" height="44" rx="4" fill="#F9F6F2" stroke="#5D4037" stroke-width="2"/>
        <rect x="14" y="16" width="10" height="32" rx="2" fill="#FFCC80" stroke="#8D6E63" stroke-width="1.5"/>
        <rect x="26" y="16" width="10" height="32" rx="2" fill="#A5D6A7" stroke="#388E3C" stroke-width="1.5"/>
        <rect x="38" y="16" width="10" height="32" rx="2" fill="#90CAF9" stroke="#1976D2" stroke-width="1.5"/>
        <rect x="14" y="28" width="34" height="2" fill="#BCAAA4"/>
        <rect x="14" y="38" width="34" height="2" fill="#BCAAA4"/>
        <rect x="14" y="48" width="34" height="2" fill="#BCAAA4"/>
        <rect x="14" y="20" width="34" height="2" fill="#BCAAA4"/>
        <rect x="14" y="10" width="34" height="2" fill="#BCAAA4"/>
        <rect x="14" y="54" width="34" height="2" fill="#BCAAA4"/>
      </svg>
      가까운 도서관 위치
    </h2>
    <div class="map-responsive">
      <div id="map" class="map-container"></div>
    </div>
  </div>

  <div v-else class="loading">책 정보를 불러오는 중입니다...</div>
</template>

<script setup>
import { ref, onMounted, computed, nextTick } from "vue";
import { useRoute, RouterLink, useRouter } from "vue-router";
import { useBookStore } from "@/stores/book.js";
import L from "leaflet";
import StarRating from "@/components/rating/StarRating.vue";

const router = useRouter()
const route = useRoute();
const bookStore = useBookStore();
const bookId = Number(route.params.bookId);



const book = computed(() => bookStore.bookDetail);
const isLiked = computed(() => book.value.liked);
const likeCount = computed(() => book.value.likes_count);
const recommendations = computed(() => bookStore.recommendationBooks);

async function onToggleLike() {
  try {
    await bookStore.toggleBookLike(bookId);
  } catch (err) {
    console.error("좋아요 처리 실패", err);
  }
}



const onMove = (bookId) => {
  router.push({ name: 'bookDetail', params: { bookId } })
    .then(() => {
      router.go(0)
    })
}
let mapInstance = null

// Overpass API로 반경 5km 내 도서관 검색
async function fetchNearbyLibraries(lat, lng) {
  const query = `
    [out:json];
    node
      ["amenity"="library"]
      (around:5000,${lat},${lng});
    out;`
  const res = await fetch('https://overpass-api.de/api/interpreter', {
    method: 'POST',
    body: query.trim()
  })
  const json = await res.json()
  return json.elements.map(el => ({
    name: el.tags.name || '이름 없는 도서관',
    address: el.tags['addr:full'] || '',
    lat: el.lat,
    lng: el.lon
  }))
}

async function initMap(lat, lng) {
  // 기존 맵이 있으면 제거
  if (mapInstance) {
    mapInstance.remove()
    mapInstance = null
  }

  // 1) 지도 생성
  mapInstance = L.map('map').setView([lat, lng], 14)
  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '© OpenStreetMap contributors'
  }).addTo(mapInstance)

  // 2) 사용자 위치 마커
  L.marker([lat, lng])
    .addTo(mapInstance)
    .bindPopup('<strong>내 위치</strong>')
    .openPopup()

  // 3) 도서관 위치 데이터 가져와서 마커 뿌리기
  const libraries = await fetchNearbyLibraries(lat, lng)
  libraries.forEach(lib => {
    L.marker([lib.lat, lib.lng])
      .addTo(mapInstance)
      .bindPopup(
        `<strong>${lib.name}</strong><br>` +
        (lib.address ? lib.address : '주소 정보 없음')
      )
  })
}

onMounted(async () => {
  // 1) 북 상세 로드 (기존 코드)
  await bookStore.getBookDetail(bookId)
  await bookStore.embeddingBook(bookId)

  // 2) 사용자 위치 얻어서 지도 초기화
  if (!navigator.geolocation) return
  navigator.geolocation.getCurrentPosition(
    async ({ coords }) => {
      await nextTick()  // v-if/v-show 렌더링 보장
      await initMap(coords.latitude, coords.longitude)
    },
    () => alert('위치 정보를 가져오지 못했습니다.')
  )
})
</script>

<style scoped>
.book-detail-view {
  max-width: 900px;
  margin: 0 auto;
  padding: 2rem;
  font-family: "Pretendard", sans-serif;
  color: #333;
}

.book-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 1rem;
  margin-bottom: 2rem;
}

.book-title {
  font-size: 2rem;
  font-weight: bold;
}

.book-header-actions {
  display: flex;
  gap: 1rem;
}

.thread-button,
.like-button {
  border: 1px solid #ccc;
  padding: 0.5rem 1rem;
  border-radius: 20px;
  background: white;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
}

.like-button.liked {
  background-color: #6c63ff;
  color: white;
  border-color: #6c63ff;
}

.book-detail-wrapper {
  display: flex;
  gap: 2rem;
  margin-bottom: 2rem;
  flex-wrap: wrap;
}

.book-cover {
  width: 200px;
  height: 300px;
  object-fit: cover;
  border-radius: 10px;
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
}

.book-text {
  flex: 1;
  min-width: 260px;
}

.book-description {
  font-size: 1rem;
  margin-bottom: 1rem;
}

.book-meta p {
  font-size: 0.9rem;
  margin: 0.2rem 0;
}

.author-title {
  font-size: 1.5rem;
  margin-top: 3rem;
  margin-bottom: 1rem;
  color: #111;
}

.author-section {
  display: flex;
  gap: 1.5rem;
  background: #f9f9f9;
  padding: 1rem;
  border-radius: 12px;
  box-shadow: 0 3px 10px rgba(0, 0, 0, 0.05);
  flex-wrap: wrap;
}

.author-photo {
  width: 100px;
  height: 100px;
  object-fit: cover;
  border-radius: 50%;
  border: 2px solid #ddd;
}

.author-text {
  flex: 1;
  min-width: 200px;
}

.map-responsive {
  margin-top: 2rem;
  border-radius: 10px;
  overflow: hidden;
  box-shadow: 0 3px 10px rgba(0, 0, 0, 0.08);
}

.map-container {
  width: 100%;
  height: 300px;
}

.loading {
  text-align: center;
  font-size: 1.2rem;
  padding: 2rem;
}

.recommendation-cards {
  display: flex;
  gap: 1rem;
  overflow-x: auto;
  padding: 1rem;
}

.card {
  flex: 0 0 20%; /* 5개 카드가 한 줄에 차지할 너비 */
  background: #fff;
  border-radius: 0.5rem;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  padding: 1rem;
  text-align: center;
}

.card-image {
  width: 100%;
  height: auto;
  border-radius: 0.25rem;
  margin-bottom: 0.5rem;
}

.card-title {
  font-size: 1.125rem;
  margin-bottom: 0.5rem;
}

.card-keywords {
  font-size: 0.875rem;
  color: #555;
}
</style>
