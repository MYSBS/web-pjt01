<template>
  <div class="interest-setting">
    <h2>관심 정보 설정</h2>

    <div class="section">
      <h3>좋아하는 작가 (최대 3명)</h3>
      <div v-for="author in uniqueAuthors" :key="author.name">
        <label>
          <input type="checkbox"
                :value="author.book"
                v-model="selectedAuthors"
                :disabled="!selectedAuthors.includes(author.book) && selectedAuthors.length >= 3">
          {{ author.name }}
        </label>
      </div>
    </div>

    <div class="section">
      <h3>관심 주제 (카테고리, 최대 3개)</h3>
      <div v-for="cat in allCategories" :key="cat.id">
        <label>
          <input type="checkbox"
                 :value="cat"
                 v-model="selectedTopics"
                 :disabled="!selectedTopics.includes(cat) && selectedTopics.length >= 3">
          {{ cat.name }}
        </label>
      </div>
    </div>

    <div class="section">
      <h3>재미있게 읽은 책 (최대 3권)</h3>
      <div v-for="book in visibleBooks" :key="book.id">
        <label>
          <input type="checkbox"
                :value="book"
                v-model="selectedBooks"
                :disabled="!selectedBooks.includes(book) && selectedBooks.length >= 3">
          {{ book.title }}
        </label>
      </div>
    </div>

    <button @click="submitInterest">저장하고 프로필로 이동</button>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useAccountStore } from '@/stores/accounts'
import axios from 'axios'

const router = useRouter()
const accountStore = useAccountStore()

const API_URL = accountStore.ACCOUNT_API_URL.replace('/accounts', '')
const BOOK_API_URL = accountStore.BOOK_API_URL

const userInfo = computed(() => accountStore.userInfo)

const allBooks = ref([])
const allCategories = ref([])

const selectedAuthors = ref([])
const selectedTopics = ref([])
const selectedBooks = ref([])

const fetchBooksAndCategories = async () => {
  const bookRes = await axios.get(`${BOOK_API_URL}/books/simple/`)
  // console.log(bookRes)
  allBooks.value = bookRes.data.slice(0, 20) 

  const catRes = await axios.get(`${BOOK_API_URL}/categories/`)
  allCategories.value = catRes.data
}

const submitInterest = () => {
  const formData = new FormData()
  selectedAuthors.value.forEach(b => formData.append('favorite_authors', b.id))
  selectedTopics.value.forEach(c => formData.append('favorite_topics', c.id))
  selectedBooks.value.forEach(b => formData.append('favorite_books', b.id))

  accountStore.updateProfile(formData)
    .then(() => {
      alert('관심 정보가 저장되었습니다.')
      router.push({ name: 'profile', params: { username: accountStore.currentUsername } })
    })
    .catch(err => {
      alert('저장 실패!')
      console.error(err)
    })
}

// 작가 10명만 중복 제거하여 가져오기
const uniqueAuthors = computed(() => {
  const seenAuthors = new Set()
  const result = []

  for (const book of allBooks.value) {
    const raw = book.author || ''
    const primaryAuthor = raw.split(',')[0].split('(')[0].trim()

    if (!seenAuthors.has(primaryAuthor)) {
      seenAuthors.add(primaryAuthor)
      result.push({ name: primaryAuthor, book })
    }

    if (result.length >= 10) break
  }

  return result
})


// 책은 앞에서 10권만 보여주기
const visibleBooks = computed(() => {
  return allBooks.value.slice(0, 10)
})

onMounted(async () => {
  await fetchBooksAndCategories()

  accountStore.getUserInfo(accountStore.currentUsername)
    .then(() => {
      selectedAuthors.value = allBooks.value.filter(book =>
        userInfo.value.favorite_authors.some(saved => saved.id === book.id)
      )
      selectedBooks.value = allBooks.value.filter(book =>
        userInfo.value.favorite_books.some(saved => saved.id === book.id)
      )
      selectedTopics.value = allCategories.value.filter(cat =>
        userInfo.value.favorite_topics.some(saved => saved.id === cat.id)
      )
    })
    .catch(err => {
      console.error('기존 관심 정보 로딩 실패:', err)
    })
})
</script>

<style scoped>
.interest-setting {
  max-width: 700px;
  margin: 3rem auto;
  padding: 2rem;
  background-color: #fdfdfd;
  border-radius: 16px;
  box-shadow: 0 6px 16px rgba(0, 0, 0, 0.06);
  font-family: 'Pretendard', sans-serif;
}

.section {
  margin-bottom: 2rem;
}

h2, h3 {
  color: #1a1a1a;
  margin-bottom: 1rem;
}

label {
  display: block;
  margin-bottom: 0.5rem;
  font-size: 0.95rem;
  color: #333;
}

button {
  background-color: #6c63ff;
  color: white;
  padding: 0.8rem 1.6rem;
  border: none;
  border-radius: 30px;
  font-size: 1rem;
  font-weight: bold;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

button:hover {
  background-color: #584ff2;
}
</style>
