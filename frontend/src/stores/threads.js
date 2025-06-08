import { ref, computed } from "vue";
import { defineStore } from "pinia";
import { useRouter } from "vue-router";
import axios from 'axios'
import { useBookStore } from "./book";
import { useAccountStore } from "./accounts";
import ThreadDetailView from "@/views/ThreadDetailView.vue";

export const useThreadStore = defineStore("thread", () => {
  const bookStore = useBookStore()
  const router = useRouter()

  const threadList = ref([])
  const threadDetail = ref([])
  const threadUsername = ref('')


const getThreads = async () => {
  try {
    // ① API 호출
    const res = await axios.get(`${bookStore.API_URL}/api/v1/threads/`)
    // ② 받은 데이터(res.data)를 그대로 할당
    threadList.value = res.data
  } catch (err) {
    console.error('스레드 목록을 불러오지 못했습니다:', err)
  }
}

const getThreadDetail = async (threadId) => {
  try {
    const tempRes = await axios.get(`${bookStore.API_URL}/api/v1/threads/${threadId}/`)
    const bookId = tempRes.data.book
    
    // 스레드 정보와 좋아요 정보를 병렬로 가져옴
    const [threadRes, likeInfo] = await Promise.all([
      axios.get(`${bookStore.API_URL}/api/v1/books/${bookId}/threads/${threadId}/`),
      getThreadLikeInfo(threadId)
    ])
    
    // 스레드 정보에 좋아요 정보 병합
    threadDetail.value = {
      ...threadRes.data,
      liked: likeInfo.liked,
      likes_count: likeInfo.likes_count
    }
    
  } catch (err) {
    console.log(err)
    router.push({name:'GenericError'})
  }
}

const getThreadUsername = async (threadId) => {
  try {
    // ① API 호출
    await getThreadDetail(threadId)
    const res = await axios.get(`${bookStore.API_URL}/api/v1/accounts/profile/getusername/${threadDetail.value.user}/`)
    threadUsername.value = res.data
  } catch (err) {
    console.log(err)

  }
}

const commentUsername = ref('')
const getCommentUsername = async (userId) => {
  try {
    // ① API 호출
    const res = await axios.get(`${bookStore.API_URL}/api/v1/accounts/profile/getusername/${userId}/`)
    commentUsername.value = res.data
  } catch (err) {
    console.log(err)

  }
}

  const makeThread = function (payload, bookId) {
    const bookStore = useBookStore()
    const accountStore = useAccountStore()
    axios({
      method: 'post',
      url: `${bookStore.API_URL}/api/v1/books/${bookId}/threads/`,
      data: payload,
      headers: {
        'Content-Type': 'multipart/form-data',
        Authorization: `Token ${accountStore.token}`
      }
    })
    .then(res =>{
      router.push({name:'threads'})
    })
    .catch(err=>{
      console.log(err)
    })
  };

  const createComment = function (threadId, payload) {
    const bookStore = useBookStore()
    const accountStore = useAccountStore()
    axios({
      method: 'post',
      url: `${bookStore.API_URL}/api/v1/books/${threadDetail.value.book.id}/threads/${threadId}/comment/`,
      data: payload,
      headers: {
        Authorization: `Token ${accountStore.token}`
      }
    })
    .then(res => {
      getThreadDetail(threadId)
    })
    .catch(err=>{
      console.log(err)
    })
  }
const updateComment = async (threadId, commentId, payload) => {
  try {
    const bookStore = useBookStore()
    const accountStore = useAccountStore()
    const res = await axios.put(
      `${bookStore.API_URL}/api/v1/books/${threadDetail.value.book.id}/threads/${threadId}/comment/${commentId}/`,
      payload,
      {
        headers: {
          Authorization: `Token ${accountStore.token}`
        }
      }
    )
    // 댓글 수정 후 스레드 상세 정보 다시 가져오기
    await getThreadDetail(threadId)
    return res.data
  } catch (err) {
    console.error('댓글 수정 실패:', err)
    throw err
  }
}

// 댓글 삭제 함수 수정
const deleteComment = async (threadId, commentId) => {
  try {
    const bookStore = useBookStore()
    const accountStore = useAccountStore()
    await axios.delete(
      `${bookStore.API_URL}/api/v1/books/${threadDetail.value.book.id}/threads/${threadId}/comment/${commentId}/`,
      {
        headers: {
          Authorization: `Token ${accountStore.token}`
        }
      }
    )
    // 댓글 삭제 후 스레드 상세 정보 다시 가져오기
    await getThreadDetail(threadId)
  } catch (err) {
    console.error('댓글 삭제 실패:', err)
    throw err
  }
}


const toggleThreadLike = async (threadId) => {
  try {
    const accountStore = useAccountStore()
    const bookStore = useBookStore()
    
    const res = await axios.post(
      `${bookStore.API_URL}/api/v1/threads/${threadId}/like/`,
      null,
      { 
        headers: { 
          Authorization: `Token ${accountStore.token}` 
        } 
      }
    )

    // 핵심: 반응형 객체 직접 업데이트
    threadDetail.value = {
      ...threadDetail.value,
      likes_count: res.data.likes_count,
      liked: res.data.liked
    }

  } catch (error) {
    console.error('좋아요 처리 실패:', error)
    alert('문제가 발생했습니다.')
  }
}


const getThreadLikeInfo = async (threadId) => {
  try {
    const accountStore = useAccountStore()
    const bookStore = useBookStore()
    
    const headers = {}
    // 로그인된 사용자라면 토큰 추가
    if (accountStore.token) {
      headers.Authorization = `Token ${accountStore.token}`
    }
    
    const res = await axios.get(
      `${bookStore.API_URL}/api/v1/threads/${threadId}/like/`,
      { headers }
    )
    
    return res.data
  } catch (error) {
    console.error('좋아요 정보 조회 실패:', error)
    return { likes_count: 0, liked: false }
  }
}


const updateThread = async (threadId, payload) => {
  try {
    const bookStore = useBookStore()
    const accountStore = useAccountStore()
    const res = await axios.put(
      `${bookStore.API_URL}/api/v1/books/${threadDetail.value.book.id}/threads/${threadId}/`,
      payload,
      {
        headers: {
          'Content-Type': 'multipart/form-data',
          Authorization: `Token ${accountStore.token}`
        }
      }
    )
    threadDetail.value = res.data
    return res.data
  } catch (err) {
    console.error('스레드 수정 실패:', err)
    throw err
  }
}

// 스레드 삭제 함수
const deleteThread = async (threadId) => {
  try {
    const bookStore = useBookStore()
    const accountStore = useAccountStore()
    await axios.delete(
      `${bookStore.API_URL}/api/v1/books/${threadDetail.value.book.id}/threads/${threadId}/`,
      {
        headers: {
          Authorization: `Token ${accountStore.token}`
        }
      }
    )
    // 삭제 후 리스트 갱신 또는 라우터 이동 처리
    threadDetail.value = null
    router.push({ name: 'threads' })
  } catch (err) {
    console.error('스레드 삭제 실패:', err)
    throw err
  }
}


  return { threadList, getThreads, makeThread, getThreadDetail, threadDetail, threadUsername, getThreadUsername,
    createComment, deleteComment, getCommentUsername, commentUsername, toggleThreadLike, getThreadLikeInfo,
    updateThread, deleteThread, updateComment
  };
});
