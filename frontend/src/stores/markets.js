import { defineStore } from 'pinia'
import axios from 'axios'
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAccountStore } from './accounts'

// API 주소 상수
const API_URL = ''
const MARKET_API_URL = `${API_URL}/api/v1/markets`

export const useMarketStore = defineStore('market', () => {
  const router = useRouter()
  const marketPosts = ref([])
  const selectedPost = ref(null)
  const comments = ref([])
  const totalCount = ref(0)
  const currentPage = ref(1)

  const accountStore = useAccountStore()
  const token = accountStore.token

  const authHeader = () => ({
    headers: {
      Authorization: `Token ${token}`
    }
  })

  // 게시글 목록 가져오기
  const fetchMarketPosts = (page = 1) => {
    return axios.get(`${MARKET_API_URL}/?page=${page}`)
      .then(res => {
      marketPosts.value = Array.isArray(res.data) ? res.data : res.data.results
      totalCount.value = res.data.count ?? res.data.length
      currentPage.value = page
    }) .catch(err => {
      router.push({name:'GenericError'})
    })
  }

  // 게시글 상세 조회
const fetchMarketPost = async (marketId) => {
  const accountStore = useAccountStore()
  const token = accountStore.token

  const res = await axios.get(`${MARKET_API_URL}/${marketId}/`, {
    headers: {
      Authorization: `Token ${token}`
    }
  })
  .then()
  .catch(()=>router.push({name:'GenericError'}))
  selectedPost.value = res.data 
  return res.data
}


  // 게시글 작성
  const createMarketPost = (formData) => {
    return axios.post(`${MARKET_API_URL}/`, formData, authHeader())
  } 

  // 게시글 수정
  const updateMarketPost = (marketId, formData) => {
    return axios.put(`${MARKET_API_URL}/${marketId}/`, formData, authHeader())
  }

  // 게시글 삭제
  const deleteMarketPost = (marketId) => {
    return axios.delete(`${MARKET_API_URL}/${marketId}/`, authHeader())
  }


  // 게시글 좋아요 토글
  const toggleMarketLike = (marketId) => {
    return axios.post(`${MARKET_API_URL}/${marketId}/like/`, null, authHeader())
      .then(res => {
        if (selectedPost.value) {
          selectedPost.value.is_liked = res.data.liked
          selectedPost.value.likes_count = res.data.likes_count
        }
        return res.data
      })
  }

  // 댓글 목록 가져오기
  const fetchComments = (marketId) => {
    return axios.get(`${MARKET_API_URL}/${marketId}/comments/`)
      .then(res => {
        comments.value = res.data.sort((a, b) => new Date(a.created_at) - new Date(b.created_at))  // 오래된 게 위로
      })
  }


  // 댓글 작성
  const submitComment = (marketId, content, replyTo = null) => {
  const data = { content }
  if (replyTo) {
    data.reply_to = replyTo
  }

  return axios.post(`${MARKET_API_URL}/${marketId}/comments/`, data, authHeader())
    .then(res => {
      comments.value.unshift(res.data)
    })
}


  // 댓글 좋아요 토글
  const toggleCommentLike = async (commentId) => {
    await axios.post(`${MARKET_API_URL}/comments/${commentId}/like/`, null, authHeader())
    await fetchComments(selectedPost.value.id)  // 댓글 전체 새로고침
  }

  // 댓글 삭제
  const deleteComment = (commentId) => {
    return axios.delete(`${MARKET_API_URL}/comments/${commentId}/`, authHeader())
      .then(() => {
        comments.value = comments.value.filter(c => c.id !== commentId)
      })
  }

  const formatDateTime = (dateStr) => {
    const date = new Date(dateStr)
    return date.toLocaleString('ko-KR', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
    })
  }


  return {
    API_URL,
    MARKET_API_URL,
    marketPosts,
    selectedPost,
    comments,
    currentPage,
    totalCount,
    fetchMarketPosts,
    fetchMarketPost,
    createMarketPost,
    updateMarketPost,
    deleteMarketPost,
    toggleMarketLike,
    fetchComments,
    submitComment,
    toggleCommentLike,
    deleteComment,
    formatDateTime,
  }
}, { persist: false })
