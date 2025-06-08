<template>
  <section class="booklist-container">
    <h1 class="page-title">Book List</h1>

    <!-- 검색창 -->
    <input
      v-model="bookStore.searchTerm"
      type="text"
      class="search-input"
      placeholder="검색어를 입력하세요..."
    />

    <!-- 카테고리 버튼 -->
    <div class="category-buttons">
      <button
        v-for="cat in bookStore.categoriesList"
        :key="cat.pk"
        @click="handleCategoryClick(cat.pk)"
        :class="['category-button', { active: bookStore.selectedCategory === cat.pk }]"
      >
        {{ cat.fields.name }}
      </button>
    </div>

    <!-- 책 목록 -->
    <ul class="book-list">
      <li
        v-for="book in paginatedBooks"
        :key="book.pk"
        class="book-card"
      >
        <RouterLink :to="`/books/${book.pk}`" class="book-link">
          <img :src="book.fields.cover" alt="표지" class="book-cover" />
          <div class="book-info">
            <h3 class="book-title">{{ book.fields.title }}</h3>
            <p class="book-meta">저자: {{ book.fields.author }}</p>
            <p class="book-meta">출판일: {{ book.fields.published_date }}</p>
            <p class="book-meta">카테고리: {{ getCategoryName(book.fields.category) }}</p>
          </div>
        </RouterLink>
      </li>
    </ul>

    <!-- 페이지네이션 -->
    <div class="pagination" v-if="totalPages > 1">
      <button
        class="arrow-btn"
        :disabled="currentPage === 1"
        @click="goToPage(currentPage - 1)"
      >
        &lt;
      </button>

      <button
        v-for="page in visiblePages"
        :key="page"
        :class="{ active: currentPage === page }"
        @click="goToPage(page)"
      >
        {{ page }}
      </button>

      <button
        class="arrow-btn"
        :disabled="currentPage === totalPages"
        @click="goToPage(currentPage + 1)"
      >
        &gt;
      </button>
    </div>
  </section>
</template>

<script setup>
import { useBookStore } from '@/stores/book.js'
import { ref, computed, onMounted } from 'vue'

const bookStore = useBookStore()

const booksPerPage = 20
const currentPage = ref(1)

const totalPages = computed(() => {
  return Math.ceil(bookStore.filteredBooks.length / booksPerPage)
})

const paginatedBooks = computed(() => {
  const start = (currentPage.value - 1) * booksPerPage
  return bookStore.filteredBooks.slice(start, start + booksPerPage)
})

const visiblePages = computed(() => {
  const pages = []
  const start = Math.max(1, currentPage.value - 5)
  const end = Math.min(totalPages.value, currentPage.value + 5)
  for (let i = start; i <= end; i++) {
    pages.push(i)
  }
  return pages
})

const goToPage = (page) => {
  currentPage.value = page
}

const getCategoryName = (categoryId) => {
  const category = bookStore.categoriesList.find(cat => cat.pk === categoryId)
  return category ? category.fields.name : '알 수 없음'
}

const handleCategoryClick = (pk) => {
  bookStore.selectedCategory = pk
  currentPage.value = 1
}


onMounted(async () => {
  await bookStore.getBooks()
})
</script>

<style scoped>
.booklist-container {
  background-color: #f8f8f8;
  padding: 2rem 1rem;
  min-height: 100vh;
}

.page-title {
  color: #111;
  text-align: center;
  margin-bottom: 2rem;
  font-family: 'Pretendard', sans-serif;
  font-size: 2rem;
}

.search-input {
  display: block;
  width: 90%;
  max-width: 500px;
  margin: 0 auto 2rem;
  padding: 0.7rem 1rem;
  border: none;
  border-radius: 12px;
  background-color: #eee;
  font-size: 1rem;
  color: #333;
  outline: none;
}

.category-buttons {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 0.5rem;
  margin-bottom: 2rem;
}

.category-button {
  padding: 0.4rem 1rem;
  border: 1px solid #ccc;
  border-radius: 20px;
  background-color: white;
  color: #333;
  font-size: 0.9rem;
  cursor: pointer;
  transition: all 0.3s ease;
}

.category-button.active,
.category-button:hover {
  background-color: #6c63ff;
  color: white;
  border-color: #6c63ff;
}

.book-list {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 2rem;
  padding: 0;
  list-style: none;
}

.book-card {
  background: white;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.06);
  overflow: hidden;
  transition: all 0.3s ease;
}

.book-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 18px rgba(0, 0, 0, 0.1);
}

.book-link {
  text-decoration: none;
  color: inherit;
  display: flex;
  flex-direction: column;
  height: 100%;
}

.book-cover {
  width: 100%;
  height: 300px;
  object-fit: cover;
  border-bottom: 1px solid #eee;
}

.book-info {
  padding: 1rem;
}

.book-title {
  font-size: 1.1rem;
  font-weight: 600;
  margin-bottom: 0.5rem;
  color: #111;
}

.book-meta {
  font-size: 0.85rem;
  color: #666;
  margin: 0.2rem 0;
}

/* Pagination 스타일 */
.pagination {
  display: flex;
  justify-content: center;
  margin-top: 2rem;
  gap: 0.5rem;
  flex-wrap: wrap;
}

.pagination button {
  background-color: white;
  border: 1px solid #ccc;
  padding: 0.5rem 0.9rem;
  border-radius: 6px;
  cursor: pointer;
  font-weight: 500;
  transition: background-color 0.3s ease;
  min-width: 40px;
}

.pagination button:hover {
  background-color: #eee;
}

.pagination button.active {
  background-color: #6c63ff;
  color: white;
  border-color: #6c63ff;
}

.arrow-btn:disabled {
  opacity: 0.4;
  cursor: not-allowed;
}
</style>
