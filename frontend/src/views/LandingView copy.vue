<template>
  <div class="hero position-relative overflow-hidden">
    <!-- 1) Hero 이미지 -->
    <img
      src="@/assets/images/hero_image.jpg"
      alt="Hero Background"
      class="hero-img"
    />

    <!-- 2) 중앙 로고 텍스트 -->
    <h1 class="hero-logo-text">
      PJT 08<br />
      AI 도서 프로젝트
    </h1>

    <!-- 3) 섹션 타이틀 -->
    <h3
      class="section-title text-white text-center position-absolute w-100"
      style="bottom: 23rem; left: 0; z-index: 20; margin: 0"
    >
      베스트셀러
    </h3>

    <!-- 4) 캐러셀 -->
    <div
      id="bestsellerCarousel"
      class="carousel slide position-absolute w-100"
      data-bs-ride="carousel"
      style="bottom: 3rem; left: 0"
    >
      <div class="carousel-inner">
        <div
          v-for="(slide, idx) in slides"
          :key="idx"
          :class="['carousel-item', { active: idx === 0 }]"
        >
          <div class="d-flex justify-content-center">
            <div
              v-for="book in slide"
              :key="book.pk"
              class="mx-3"
              style="width: 200px"
            >
              <RouterLink
                :to="`/books/${book.pk}`"
                class="text-decoration-none"
                @click="selectedBook = book.pk"
              >
                <div
                  class="book-card"
                  :class="{ active: selectedBook === book.pk }"
                >
                  <img
                    :src="book.fields.cover"
                    class="book-img"
                    alt="표지"
                  />
                  <div class="book-info">
                    <p class="book-title text-center">
                      {{ book.fields.title }}
                    </p>
                  </div>
                </div>
              </RouterLink>
            </div>
          </div>
        </div>
      </div>

      <!-- Prev / Next 버튼 -->
      <button
        class="carousel-control-prev"
        type="button"
        data-bs-target="#bestsellerCarousel"
        data-bs-slide="prev"
      >
        <span class="carousel-control-prev-icon"></span>
        <span class="visually-hidden">Previous</span>
      </button>
      <button
        class="carousel-control-next"
        type="button"
        data-bs-target="#bestsellerCarousel"
        data-bs-slide="next"
      >
        <span class="carousel-control-next-icon"></span>
        <span class="visually-hidden">Next</span>
      </button>
    </div>
  </div>
</template>

<script setup>
import { computed, onMounted, ref } from 'vue'
import { RouterLink } from 'vue-router'
import { useBookStore } from '@/stores/book.js'

const bookstore = useBookStore()
onMounted(() => {
  bookstore.getBooks()
})

const selectedBook = ref(null)

const CHUNK = 4
const bestseller = computed(() =>
  [...bookstore.bookList]
    .sort((a, b) => b.fields.customer_review_rank - a.fields.customer_review_rank)
    .slice(0, 12)
)
const slides = computed(() => {
  const arr = []
  for (let i = 0; i < bestseller.value.length; i += CHUNK) {
    arr.push(bestseller.value.slice(i, i + CHUNK))
  }
  return arr
})
</script>

<style scoped>
.hero {
  position: relative;
  width: 100%;
  height: 100vh;
  overflow: hidden;
  background-color: #000;
}

.hero-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  opacity: 0.35;
}

.hero-logo-text {
  position: absolute;
  top: 40%;
  left: 50%;
  transform: translate(-50%, -50%);
  font-size: 3.5rem;
  font-weight: 700;
  color: white;
  text-align: center;
  z-index: 10;
}

.section-title {
  font-size: 1.6rem;
  font-weight: 600;
  letter-spacing: 1px;
}

.book-card {
  background-color: white;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
  cursor: pointer;
  border: 2px solid transparent;
}

.book-card:hover {
  transform: translateY(-6px) scale(1.03);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.2);
  border-color: #6c63ff;
}

.book-card.active {
  border-color: #6c63ff;
  box-shadow: 0 8px 28px rgba(108, 99, 255, 0.5);
  transform: scale(1.05);
}

.book-img {
  width: 100%;
  height: 260px;
  object-fit: cover;
}

.book-title {
  font-size: 1rem;
  font-weight: 500;
  color: #333;
  margin: 0.5rem 0;
}

@media (max-width: 768px) {
  .hero-logo-text {
    font-size: 2rem;
  }

  .book-img {
    height: 200px;
  }

  .book-card {
    margin: 0 0.5rem;
  }
}
</style>
