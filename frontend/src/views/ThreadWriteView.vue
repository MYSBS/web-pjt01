<template>
  <div class="my-modal">
    <h2 class="modal-title">새로운 포스트 작성</h2>

    <!-- 제목 -->
    <div class="form-group">
      <p>제목</p>
      <input
        type="text"
        class="input"
        placeholder="제목을 작성해주세요"
        v-model="inputTitle"
      />
    </div>

    <!-- 내용 -->
    <div class="form-group">
      <p>내용</p>
      <textarea
        class="textarea"
        rows="6"
        placeholder="내용을 입력해 주세요"
        v-model="inputContent"
      ></textarea>

      <!-- AI 보완 버튼 -->
      <button
        type="button"
        class="btn ai-btn btn-info"
        :disabled="loadingEnhance"
        @click="onAIEnhance"
      >
        {{ loadingEnhance ? '보완 중…' : 'AI 보완' }}
      </button>

      <!-- 수정 가능한 보완 텍스트 영역 -->
      <div v-if="enhancedContent" class="enhanced-section">
        <p>보완된 내용 (수정 가능)</p>
        <textarea
          class="textarea"
          rows="6"
          v-model="enhancedContent"
        ></textarea>
        <button
          type="button"
          class="btn btn-success"
          @click="applyEnhanced"
        >
          본문에 반영
        </button>
      </div>

      <!-- diff 뷰 -->
      <!-- <div v-if="diffResult" class="diff-view">
        <h4>-Before  +After</h4>
        <pre class="diff-output">{{ diffResult }}</pre>
      </div> -->
    </div>

    <!-- 읽은 날짜 -->
    <div class="form-group">
      <p>읽은 날짜</p>
      <input
        type="date"
        class="date-input"
        v-model="inputDate"
      />
    </div>

    <!-- 이미지 업로드 -->
    <div class="form-group">
      <p>이미지 (선택)</p>
      <input
        type="file"
        class="input"
        accept="image/*"
        ref="selectedFile"
        @change="onFileChange"
      />
      <p v-if="selectedFile" class="text-info">
        선택된 파일: {{ selectedFile.name }}
      </p>
      <p v-else class="text-secondary">
        파일이 선택되지 않았습니다.
      </p>
      <div v-if="previewUrl" class="img-preview">
        <img
          :src="previewUrl"
          alt="미리보기"
          class="preview-img"
        />
      </div>
    </div>

    <!-- 도서 정보 -->
    <p>도서 정보</p>
    <div v-if="nowBook" class="book-section">
      <div class="book-card">
        <img
          class="book-cover"
          :src="nowBook.cover"
          alt="도서 이미지"
        />
        <div class="book-title">{{ nowBook.title }}</div>
        <div class="book-detail">
          {{ nowBook.title }} | {{ nowBook.publisher }} | {{ nowBook.pub_date }}
        </div>
        <div class="book-meta">{{ nowBook.subTitle }}</div>
      </div>
    </div>

    <div v-else>도서 정보를 불러오는 중입니다…</div>

    <!-- 버튼 -->
    <div class="button-group">
      <button class="btn cancel" @click="goBack">취소</button>
      <button class="btn submit" @click="onMakeThread">확인</button>
    </div>
  </div>
</template>

<script setup>
import { ref, onUnmounted, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useThreadStore } from '@/stores/threads'
import { useBookStore } from '@/stores/book'
import defaultImg from '@/assets/images/defaultimg.png'
import axios from 'axios'

const route = useRoute()
const router = useRouter()
const threadStore = useThreadStore()
const bookStore = useBookStore()

const nowBook = ref(null)

const bookId = Number(route.params.bookId)
onMounted(async ()=> {
  bookStore.getBookDetail(bookId)
})
nowBook.value = bookStore.bookDetail

// form state
const inputTitle      = ref('')
const inputContent    = ref('')
const inputDate       = ref('')

// file upload state
const selectedFile    = ref(null)
const previewUrl      = ref('')

// AI 보완 상태
const loadingEnhance  = ref(false)
const enhancedContent = ref('')
const diffResult      = ref('')

function onFileChange(e) {
  const file = e.target.files[0] || null
  selectedFile.value = file

  if (file) {
    previewUrl.value = URL.createObjectURL(file)
  } else {
    previewUrl.value = defaultImg
  }
}

onUnmounted(() => {
  if (previewUrl.value) {
    URL.revokeObjectURL(previewUrl.value)
  }
})

function goBack() {
  router.back()
}


    const onMakeThread = () => {
      if (!inputTitle.value || !inputContent.value || !inputDate.value) {
        return alert('모든 필수 항목을 입력해 주세요.')
      }
      const form = new FormData()
      form.append('title',        inputTitle.value)
      form.append('content',      inputContent.value)
      form.append('reading_date', inputDate.value)
      const file = selectedFile.value.files[0]
      if (file) {
        form.append('cover_img', file)
      }

      threadStore.makeThread(form, bookId)
        .then(() => {
          router.push({ name: 'threads' })
        })
        .catch(err => {
          console.error(err)
          alert('스레드 생성에 실패했습니다.')
        })
    }


async function onAIEnhance() {
  if (!inputContent.value.trim()) {
    return alert('내용을 입력한 후 시도해주세요.')
  }
  loadingEnhance.value = true
  try {
    const { data } = await axios.post(
      `${bookStore.API_URL}/api/v1/books/${bookId}/enhance/`,
      { content: inputContent.value }
    )
    enhancedContent.value = data.enhancedContent
    diffResult.value      = data.diffResult
  } catch (err) {
    console.error(err)
    alert('AI 보완 중 오류가 발생했습니다.')
  } finally {
    loadingEnhance.value = false
  }
}
function applyEnhanced() {
  inputContent.value = enhancedContent.value
}


</script>


<style scoped>
  .my-modal {
    max-width: 700px;
    margin: 2rem auto;
    padding: 24px;
    background: #fff;
    border-radius: 12px;
    box-shadow: 0 4px 20px rgba(0,0,0,0.1);
    font-family: 'Noto Sans KR', sans-serif;
  }

  /* 헤더 */
  .modal-title {
    font-size: 1.5rem;
    font-weight: bold;
    text-align: center;
    margin-bottom: 1.25rem;
    color: #333;
  }

  /* 폼 그룹 */
  .form-group {
    margin-bottom: 1rem;
  }
  .form-group p {
    margin: 0 0 0.5rem;
    font-weight: 500;
    color: #444;
  }

  /* 입력 필드 */
  .input,
  .textarea,
  .date-input {
    width: 100%;
    padding: 0.75rem 1rem;
    font-size: 0.95rem;
    border: 1px solid #ccc;
    border-radius: 8px;
    box-sizing: border-box;
    background-color: #f9f9fc;
  }
  .textarea {
    resize: vertical;
  }

  /* 파일 안내 */
  .text-info {
    margin-top: 0.5rem;
    color: #6c63ff;
  }
  .text-secondary {
    margin-top: 0.5rem;
    color: #aaa;
  }

  /* 이미지 미리보기 */
  .img-preview {
    margin-top: 0.75rem;
    text-align: center;
  }
  .preview-img {
    max-width: 100%;
    max-height: 200px;
    border-radius: 8px;
    box-shadow: 0 2px 6px rgba(0,0,0,0.08);
  }

  /* 도서 정보 카드 */
  .book-section {
    margin: 2rem 0;
    display: flex;
    justify-content: center;
  }
  .book-card {
    background: #fafafa;
    padding: 1rem;
    border-radius: 8px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.06);
    max-width: 360px;
  }
  .book-cover {
    width: 80px;
    border-radius: 4px;
    margin-bottom: 0.5rem;
  }
  .book-title {
    font-size: 1rem;
    font-weight: bold;
    margin-bottom: 0.25rem;
  }
  .book-detail,
  .book-meta {
    font-size: 0.875rem;
    color: #666;
    margin-bottom: 0.25rem;
  }

  /* 버튼 그룹 */
  .button-group {
    display: flex;
    gap: 1rem;
    margin-top: 2rem;
  }
  .btn {
    flex: 1;
    padding: 0.75rem 0;
    font-size: 1rem;
    border: none;
    border-radius: 8px;
    cursor: pointer;
    transition: background-color 0.2s, transform 0.1s;
  }
  .btn.cancel {
    background: #aaa;
    color: white;
  }
  .btn.cancel:hover {
    background: #888;
  }
  .btn.submit {
    background: #6c63ff;
    color: white;
    font-weight: bold;
  }
  .btn.submit:hover {
    transform: translateY(-2px);
    background-color: #584ff2;
  }
  .btn-success {
    background: #6c63ff;
    color: white;
    margin-top: 0.5rem;
  }

  /* 포커스 시 강조 */
  .input:focus,
  .textarea:focus,
  .date-input:focus {
    outline: none;
    border-color: #6c63ff;
    box-shadow: 0 0 0 3px rgba(108,99,255,0.3);
  }

  /* 보완 섹션 */
  .enhanced-section {
    margin-top: 1rem;
  }

  .ai-btn {
    background-color: #6c63ff;  /* 기존 테마색 */
    color: white;
    padding: 0.6rem 1.2rem;
    border: none;
    border-radius: 8px;
    font-weight: 500;
    margin-top: 0.5rem;
    transition: background-color 0.3s;
  }

  .ai-btn:hover {
    background-color: #584ff2;
  }

</style>