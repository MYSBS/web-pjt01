<template>
  <div class="interest-container">
    <h3>💡 관심 정보</h3>

    <!-- 좋아하는 작가 -->
    <div class="section">
      <h4>좋아하는 작가</h4>
      <div v-if="!profileInfo.favorite_authors?.length" class="empty-message">
        아직 등록한 작가가 없어요.
      </div>
      <div v-else class="tag-list">
        <span
          v-for="author in profileInfo.favorite_authors"
          :key="author.id"
          class="interest-tag"
        >
          {{ authorTrimmer(author.author) }}
           <!-- ({{ author.title }}) -->
        </span>
      </div>
    </div>

    <!-- 관심 주제 -->
    <div class="section">
      <h4>관심 주제</h4>
      <div v-if="!profileInfo.favorite_topics?.length" class="empty-message">
        아직 관심 주제를 등록하지 않았어요.
      </div>
      <div v-else class="tag-list">
        <span
          v-for="topic in profileInfo.favorite_topics"
          :key="topic.id"
          class="interest-tag"
        >
          {{ topic.name }}
        </span>
      </div>
    </div>

    <!-- 재미있게 읽은 책 -->
    <div class="section">
      <h4>재미있게 읽은 책</h4>
      <div v-if="!Array.isArray(profileInfo.favorite_books) || profileInfo.favorite_books.length === 0" class="empty-message">
        아직 등록한 책이 없어요.
      </div>
      <div v-else class="book-text-list">
        <div
          v-for="book in profileInfo.favorite_books"
          :key="book.id"
          class="book-entry interest-tag"
        >
          {{ book.title }}    -    {{ book.author }}
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useAccountStore } from '@/stores/accounts'

const accountStore = useAccountStore()
const profileInfo = computed(() => accountStore.userInfo)

const authorTrimmer = (name) => {
  if (!name) return ''
  return name.split(',')[0].split('(')[0].trim()
}
</script>

<style scoped>
.interest-container {
  max-width: 960px;
  margin: 3rem auto;
  padding: 1rem;
  font-family: 'Pretendard', sans-serif;
  animation: fadeIn 0.4s ease-in-out;
}

h3 {
  font-size: 1.6rem;
  margin-bottom: 2rem;
  color: #1a1a1a;
}

.section {
  margin-bottom: 2.5rem;
}

h4 {
  font-size: 1.2rem;
  font-weight: 600;
  color: #333;
  margin-bottom: 0.8rem;
}

.empty-message {
  color: #888;
  font-size: 0.95rem;
  margin-bottom: 1rem;
}

/* ✨ 말풍선/태그 스타일 */
.tag-list {
  display: flex;
  flex-wrap: wrap;
  gap: 0.6rem;
}

.interest-tag {
  background-color: #f0f0f0;
  padding: 0.5rem 1rem;
  border-radius: 20px;
  font-size: 0.95rem;
  color: #333;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.04);
}

/* 📚 책 텍스트 스타일 */
.book-text-list {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  padding-left: 0.5rem;
}

.book-entry {
  font-size: 0.95rem;
  color: #444;
  line-height: 1.6;
}

/* ✨ 애니메이션 */
@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
</style>
