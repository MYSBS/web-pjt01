import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { defineStore } from 'pinia'
import axios from 'axios'
import { useAccountStore } from './accounts'


export const useBookStore = defineStore('book', () => {
  const router = useRouter()
  const bookList = ref([])
  const categoriesList = ref([])
  const API_URL = ''
  const bookDetail = ref(null)


  const getBooks = function() {
    axios({
      method: 'get',
      url: `${API_URL}/api/v1/books/`
    })
    .then(res =>{
      bookList.value = res.data.books
      categoriesList.value = res.data.categories
    })
    .catch(err=>{
      console.log(err)
      router.push({name:'GenericError'})
    })
  }

  
const getBookDetail = async (bookId) => {
  try {
    // 책 정보와 좋아요 정보를 병렬로 가져옴
    const [bookRes, likeInfo] = await Promise.all([
      axios.get(`${API_URL}/api/v1/books/${bookId}/`),
      getBookLikeInfo(bookId)
    ])
    
    // 책 정보에 좋아요 정보 병합
    bookDetail.value = {
      ...bookRes.data,
      liked: likeInfo.liked,
      likes_count: likeInfo.likes_count
    }
    
    return bookDetail.value
  } catch (err) {
    console.error('책 상세 정보를 불러오는데 실패했습니다:', err)
    router.push({name:'GenericError'})
  }
}

  // 카테고리 및 검색 (기본은 전체)
  const selectedCategory = ref(0)
  const searchTerm = ref('')

  const filteredBooks = computed(() => {
    return bookList.value.filter((book) => {
      const matchCategory =
        selectedCategory.value === 0 ||
        book.fields.category === selectedCategory.value

      const matchSearch =
        book.fields.title.includes(searchTerm.value) ||
        book.fields.author.includes(searchTerm.value)

      return matchCategory && matchSearch
    })
  })

const toggleBookLike = async (bookId) => {
  try {
    const accountStore = useAccountStore()
    
    // 로그인 체크
    if (!accountStore.token) {
      alert('로그인이 필요합니다.')
      return
    }
    
    const res = await axios.post(
      `${API_URL}/api/v1/books/${bookId}/like/`,
      null,
      { 
        headers: { 
          Authorization: `Token ${accountStore.token}` 
        } 
      }
    )

    // 상태 업데이트
    bookDetail.value = {
      ...bookDetail.value,
      likes_count: res.data.likes_count,
      liked: res.data.liked
    }

  } catch (error) {
    console.error('좋아요 처리 실패:', error)
    if (error.response?.status === 401) {
      alert('로그인이 필요합니다.')
    } else {
      alert('문제가 발생했습니다.')
    }
  }
}


// 책 추천
 // 추천 관련 추가
  const gptBooks = ref([])
  const hasRecommendation = ref(false)
  const recommendationStatus = ref('none')

  const fetchRecommendation = async () => {
    const accountStore = useAccountStore()
    const token = accountStore.token

    const res = await axios.get(`${API_URL}/api/v1/accounts/recommend/gpt/`, {
      headers: { Authorization: `Token ${token}` }
    })

    const recs = res.data?.recommendations

    gptBooks.value = Array.isArray(recs) ? recs : []

    recommendationStatus.value = gptBooks.value.length > 0 ? 'exists' : 'empty'
    hasRecommendation.value = true
  }

  const createRecommendation = async () => {
    const accountStore = useAccountStore()
    const token = accountStore.token

    const res = await axios.post(`${API_URL}/api/v1/accounts/recommend/gpt/`, null, {
      headers: { Authorization: `Token ${token}` }
    })
    gptBooks.value = res.data.recommendations
    recommendationStatus.value = 'exists'
    hasRecommendation.value = true
  }

  const nowLike = ref(false)

  const getBookLikeInfo = async (bookId) => {
    const accountStore = useAccountStore()
    const headers = {}
    if (accountStore.token) {
      headers.Authorization = `Token ${accountStore.token}`
    }

    const res = await axios.get(
      `${API_URL}/api/v1/books/${bookId}/like/`,
      { headers }
    )

    nowLike.value = res.data.liked
    return res.data
  }

  // 마켓에서 이용
  const getSimpleBookList = function () {
    return axios.get(`${API_URL}/api/v1/books/`)
      .then(res => res.data.books)
      .catch(err => {
        console.error('책 목록 가져오기 실패:', err)
        return []
      })
  }



  // 별점 정보
  const userRating    = ref(0)
  const averageRating = ref(0)

  async function fetchBookRating(bookId) {
    const accountStore = useAccountStore()
    if (!accountStore.token) {
      userRating.value = 0
      averageRating.value = 0
      return
    }
    const res = await axios.get(
      `${API_URL}/api/v1/books/${bookId}/rating/`,
      { headers: { Authorization: `Token ${accountStore.token}` } }
    )
    userRating.value    = res.data.user_score ?? 0
    averageRating.value = res.data.average_score
  }

  // ─────────── 별점 등록/수정 ───────────
  async function submitBookRating(bookId, score) {
    const accountStore = useAccountStore()
    if (!accountStore.token) {
      alert('로그인이 필요합니다.')
      return
    }
    const res = await axios.post(
      `${API_URL}/api/v1/books/${bookId}/rating/`,
      { score },
      { headers: { Authorization: `Token ${accountStore.token}` } }
    )
    userRating.value    = res.data.user_score
    averageRating.value = res.data.average_score

    // bookDetail에도 반영
    if (bookDetail.value && bookDetail.value.id === bookId) {
      bookDetail.value.customer_review_rank = res.data.average_score
    }
  }

  const recommendationBooks = ref(null)
  async function embeddingBook(bookId) {
    try {
      // URL 파라미터에서 책 ID 가져오기
      if (!bookId) {
        throw new Error('책 ID가 없습니다.')
      }

      // 상세 정보 요청
      await getBookDetail(bookId)
      const embedding = bookDetail.value.embedding

      // 추천 API 요청
      const res = await axios.post(
        `${API_URL}/api/v1/recommend/embb`,
        { embedding }
      )
      recommendationBooks.value = res.data
    } catch (err) {
      console.error('추천 도서 로드 실패:', err)
    }
  }



  return { 
    bookList, 
    bookDetail,
    API_URL,
    getBooks,
    getBookDetail,
    categoriesList,
    selectedCategory,
    searchTerm,
    filteredBooks,
    toggleBookLike,
    
    recommendations: gptBooks,
    hasRecommendation, 
    fetchRecommendation, 
    createRecommendation,
    recommendationStatus,
    getSimpleBookList,

    getBookLikeInfo,
    nowLike,

    userRating,
    averageRating,
    fetchBookRating,
    submitBookRating,

    recommendationBooks,
    embeddingBook
  }
})

