<template>
  <!-- nowThread 가 채워졌을 때만 전체 렌더 -->
  <div v-if="nowThread">
    <!-- 전체 thread 영역 -->
    <div class="thread-detail">


      <!-- 스레드 본문 -->
      <article class="thread-content" v-if="nowThread">
        <div class="thread-header">
          <h1>{{ nowThread.title }}</h1>
          <!-- 수정/삭제 버튼 (작성자만 볼 수 있음) -->
          <div class="thread-actions" v-if="canEditThread">
            <button class="edit-btn" @click="toggleEditMode">
              {{ isEditing ? '취소' : '수정' }}
            </button>
            <button class="delete-btn" @click="onDeleteThread">
              삭제
            </button>
          </div>
        </div>

        <!-- 작성자 정보 + 프로필 이미지 -->
        <h4 class="author-line">
          <img
            v-if="nowUser.profile_img"
            :src="
              nowUser.profile_img.startsWith('http')
                ? nowUser.profile_img
                : `${bookStore.API_URL}${nowUser.profile_img}`
            "
            alt="작성자 프로필"
            class="author-avatar"
            @click="moveUserProfile(nowUser.username)"
          />
          <img
            v-else
            src="./../../src/assets/images/defaultimg.png"
            alt="작성자 프로필"
            class="author-avatar"
            @click="moveUserProfile(nowUser.username)"
          />
        <span
          class="clickable author-name"
          @click="moveUserProfile(nowUser.username)"
        >
          {{ nowUser.username }}
        </span></h4><h4>
        <p class="post-time">{{ formatDateTime(nowThread.created_at) }}</p>
        </h4>

        <!-- 수정 모드일 때 폼 표시 -->
        <div v-if="isEditing" class="edit-form">
          <input 
            v-model="editForm.title" 
            class="edit-title"
            placeholder="제목을 입력하세요"
          />
          <textarea 
            v-model="editForm.content" 
            class="edit-content"
            placeholder="내용을 입력하세요"
            rows="10"
          ></textarea>
          <input 
            type="file" 
            @change="onFileChange"
            accept="image/*"
            class="edit-file"
          />
          <div class="edit-actions">
            <button class="save-btn" @click="onUpdateThread">저장</button>
            <button class="cancel-btn" @click="toggleEditMode">취소</button>
          </div>
        </div>

        <!-- 일반 보기 모드 -->
        <div v-else class="thread-text">
          <p v-for="(line, i) in contentLines" :key="i">
            {{ line }}
          </p>

          <div v-if="nowThread.cover_img" class="uploaded-image">
            <img
              :src="nowThread.cover_img.startsWith('http') ? nowThread.cover_img : `${bookStore.API_URL}${nowThread.cover_img}`"
              alt="업로드 이미지"
              class="uploaded-img"
            />
          </div>
        </div>
      </article>

      <!-- 좋아요 버튼 -->
      <button
        class="like-button"
        :class="{ liked }"
        @click="onToggleLike"
      >
        {{ liked ? '💔 좋아요 취소' : '❤️ 좋아요' }}
        <span>({{ likesCount }})</span>
      </button>
    </div>
          <!-- 책 정보가 있을 때만 사이드바 -->
      <aside class="book-section" v-if="nowBook">
        <div class="book-card">
          <img
            class="book-cover"
            :src="nowBook.cover"
            alt="도서 이미지"
          />
          <div class="book-title">{{ nowBook.title }}</div>
          <div class="book-detail">
            {{ nowBook.author }} | {{ nowBook.publisher }} | {{ nowBook.pub_date }}
          </div>
          <div class="book-meta">{{ nowBook.subTitle }}</div>
        </div>
      </aside>
  </div>

  <!-- 로딩 시 -->
  <div v-else class="loading">
    스레드를 불러오는 중입니다...
  </div>

  <!-- 댓글 컴포넌트 -->
  <CommentsSection />
</template>

<script setup>
import defaultImg from '@/assets/images/defaultimg.png'
import { ref, onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useThreadStore } from '@/stores/threads'
import { useBookStore } from '@/stores/book'
import { useAccountStore } from '@/stores/accounts'
import CommentsSection from '@/components/comments/CommentsSection.vue'

const route = useRoute()
const router = useRouter()
const threadStore = useThreadStore()
const bookStore = useBookStore()
const accountStore = useAccountStore()

const threadId = Number(route.params.threadId)

// 수정 관련 상태
const isEditing = ref(false)
const editForm = ref({
  title: '',
  content: '',
  cover_img: null
})

const nowThread = computed(() => threadStore.threadDetail)
const nowBook = computed(() => nowThread.value.book) 
const nowUser = computed(() => threadStore.threadUsername)
const liked = computed(() => nowThread.value.liked)
const likesCount = computed(() => nowThread.value.likes_count)

// 현재 사용자가 스레드를 수정할 수 있는지 확인
const canEditThread = computed(() => {
  return accountStore.isLogin && 
         nowUser.value && 
         accountStore.currentUsername && 
         nowUser.value.username === accountStore.currentUsername
})

// 안전하게 content split 처리
const contentLines = computed(() => {
  const content = nowThread.value?.content
  return typeof content === 'string' ? content.split('\n') : []
})

const formatDateTime = (dateString) => {
  const date = new Date(dateString)
  return date.toLocaleString('ko-KR', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit',
    hour12: false
  })
}


onMounted(async () => {
  await threadStore.getThreadUsername(route.params.threadId)
  
  // 현재 사용자 정보가 없으면 가져오기
  if (accountStore.isLogin && !accountStore.currentUser) {
    await accountStore.getCurrentUser()
  }
})

const moveUserProfile = function (username) {
  router.push({name:'profile', params: {username}})
}

async function onToggleLike() {
  try {
    await threadStore.toggleThreadLike(threadId)
  } catch (err) {
    console.error(err)
  }
}

// 수정 모드 토글
const toggleEditMode = () => {
  if (!isEditing.value) {
    // 수정 모드로 전환할 때 현재 값으로 폼 초기화
    editForm.value = {
      title: nowThread.value.title,
      content: nowThread.value.content,
      cover_img: null
    }
  }
  isEditing.value = !isEditing.value
}

// 파일 변경 처리
const onFileChange = (event) => {
  const file = event.target.files[0]
  if (file) {
    editForm.value.cover_img = file
  }
}

// 스레드 수정
const onUpdateThread = async () => {
  try {
    const formData = new FormData()
    formData.append('title', editForm.value.title)
    formData.append('content', editForm.value.content)
    
    if (editForm.value.cover_img) {
      formData.append('cover_img', editForm.value.cover_img)
    }

    await threadStore.updateThread(threadId, formData)
    isEditing.value = false
    alert('스레드가 수정되었습니다.')
  } catch (err) {
    console.error('수정 실패:', err)
    alert('수정에 실패했습니다.')
  }
}

// 스레드 삭제
const onDeleteThread = async () => {
  if (confirm('정말로 이 스레드를 삭제하시겠습니까?')) {
    try {
      await threadStore.deleteThread(threadId)
      alert('스레드가 삭제되었습니다.')
    } catch (err) {
      console.error('삭제 실패:', err)
      alert('삭제에 실패했습니다.')
    }
  }
}
</script>

<style scoped>
.thread-wrapper {
  max-width: 960px;
  margin: 4rem auto;
  padding: 2rem;
  font-family: 'Pretendard', sans-serif;
  display: flex;
  flex-direction: column;
  gap: 2rem;
  background-color: #fff;
  border-radius: 16px;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.05);
}

.cover-section {
  text-align: center;
  margin-bottom: 2rem;
}

.main-cover {
  max-width: 100%;
  height: auto;
  border-radius: 16px;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.1);
}

.thread-detail {
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

.book-section {
  display: flex;
  align-items: flex-start;
  gap: 1.5rem;
  justify-content: flex-start;
}

.book-card {
  display: flex;
  align-items: flex-start;
  gap: 1rem;
  background-color: #fafafa;
  border-radius: 12px;
  padding: 1.5rem;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.03);
}

.book-cover {
  width: 100px;
  height: 140px;
  object-fit: cover;
  border-radius: 8px;
}

.book-title {
  font-weight: bold;
  font-size: 1.2rem;
  margin-bottom: 0.3rem;
}

.book-detail,
.book-meta {
  font-size: 0.9rem;
  color: #666;
}

.thread-header {
  font-size: 1.5rem;
  font-weight: 700;
  text-align: center;
}

.meta-line {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.9rem;
  color: #555;
  justify-content: center;
}

.author-avatar {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  object-fit: cover;
  border: 1px solid #ccc;
}

.author-name {
  font-weight: 600;
  color: #6c63ff;
  cursor: pointer;
}

.author-line {
  display: flex;
  justify-content: flex-end;
  align-items: center;  /* 세로 가운데 정렬 */
  gap: 0.5rem;           /* 아바타와 이름 사이 간격 */
  margin-top: 1rem;
}
.thread-actions {
  display: flex;
  justify-content: flex-end;
  gap: 8px;
}

.edit-btn,
.delete-btn {
  padding: 0.4rem 0.8rem;
  border-radius: 8px;
  font-size: 0.9rem;
  cursor: pointer;
  border: none;
}

.edit-btn {
  background-color: #6c63ff;
  color: #fff;
}

.delete-btn {
  background-color: #f44336;
  color: white;
}

.edit-title,
.edit-content {
  width: 100%;
  padding: 0.75rem;
  margin-bottom: 1rem;
  border: 1px solid #ddd;
  border-radius: 8px;
  font-size: 1rem;
}

.edit-content {
  resize: vertical;
  min-height: 200px;
}

.save-btn,
.cancel-btn {
  padding: 0.6rem 1.2rem;
  border-radius: 8px;
  font-size: 0.9rem;
  font-weight: 600;
  border: none;
  cursor: pointer;
}

.save-btn {
  background-color: #2196f3;
  color: #fff;
}

.cancel-btn {
  background-color: #888;
  color: #fff;
}

.like-button {
  align-self: flex-end;
  padding: 0.6rem 1rem;
  border-radius: 30px;
  background-color: #6c63ff;
  color: white;
  border: none;
  font-size: 1rem;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.like-button.liked {
  background-color: #e91e63;
}

.like-button:hover {
  background-color: #584ff2;
}

.loading {
  text-align: center;
  color: #999;
  font-size: 1.2rem;
  padding: 2rem;
}

.thread-text {
  margin-bottom: 1rem;
  line-height: 1.6;
  font-size: 1rem;
  color: #333;
  padding-left: 1rem; 
}

.uploaded-image {
  margin-top: 1.5rem;
  display: flex;
  justify-content: center;
}

.uploaded-img {
  width: 200px;
  height: auto;
  object-fit: cover;
  border-radius: 12px;
  box-shadow: 0 6px 16px rgba(0, 0, 0, 0.08);
}
.post-time {
  font-size: 0.8rem;
  color: #86868b;
  margin: 0.25rem 0 0 0;
  text-align: right;
}

</style>
