import axios from 'axios'
import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import { useRouter } from 'vue-router'

export const useAccountStore = defineStore('account', () => {
  // 아래 한개 url 만 바꿔주면 됩니다 
  const API_URL = ''
  const BOOK_API_URL = `${API_URL}/api/v1`
  const ACCOUNT_API_URL = `${API_URL}/api/v1/accounts`

  const token = ref(null)
  const currentUsername = ref(null)
  const userInfo = ref(null)
  const currentUser = ref(null)
  const router = useRouter()

  const isLogin = computed(() => !!token.value)

  const getUserInfo = (username) => {
    return axios.get(`${ACCOUNT_API_URL}/profile/${username}/`, {
      headers: { Authorization: `Token ${token.value}` },
    }).then(res => {
      userInfo.value = res.data
      return res.data
    }).catch(err => {
      console.error('프로필 fetch 실패:', err)
      router.push({name:'GenericError'})
    })
  }

const signUp = (payload) => {
  return axios.post(`${ACCOUNT_API_URL}/signup/`, payload)
    .then(res => {
      // console.log('회원가입 성공:', res.data)
      router.push({ name: 'login' })  // 로그인 페이지로 이동
      return res
    })
    .catch(err => {
      // console.error('회원가입 실패:', err.response?.data)
      throw err
    })

}

  const logIn = ({ username, password }) => {
    return axios.post(`${ACCOUNT_API_URL}/login/`, { username, password })
      .then(res => {
        token.value = res.data.key
        currentUsername.value = username

        return res
      })
      .catch(err => {
        console.log(err)
        throw err
      })
  }

  const logOut = () => {
    axios.post(`${ACCOUNT_API_URL}/logout/`)
      .then(() => {
        token.value = null
        currentUsername.value = null
        currentUser.value = null

        localStorage.removeItem('token')  // 혹시 남아있는 토큰 삭제
        localStorage.removeItem('account')  // Pinia persist 저장소 제거

        console.log('로그아웃 성공')
        router.push({ name: 'landing' })
      })
      .catch(err => {
        console.log(err)
      })
  }


  const profile = (username) => {
    return axios.get(`${ACCOUNT_API_URL}/profile/${username}/`, {
      headers: { Authorization: `Token ${token.value}` },
    }).then(res => res.data)
      .catch(err => {
        console.error('프로필 페이지 불러오기 실패:', err)
        throw err
      })
  }

  const updateProfile = (formData) => {
    return axios.put(`${ACCOUNT_API_URL}/profile/update/`, formData, {
      headers: { Authorization: `Token ${token.value}` },
    }).then(res => res.data)
      .catch(err => {
        console.error('프로필 수정 실패:', err)
        return null
      })
  }

  const updateInterests = (payload) => {
    return axios.put(`${ACCOUNT_API_URL}/profile/update/`, payload, {
      headers: { Authorization: `Token ${token.value}` },
    }).then(res => {
      userInfo.value = res.data
      
      return getUserInfo(res.data.username)
    }).catch(err => {
      console.error('관심정보 수정 실패:', err)
      throw err
    })
  }

  const loadSimpleBookList = () => {
    return axios.get(`${BOOK_API_URL}/books/simple/`)
      .then(res => res.data)
      .catch(err => {
        console.error('책 목록 가져오기 실패:', err.message)
        throw err
      })
  }

  const getCurrentUser = () => {
    if (!token.value || !currentUsername.value) return Promise.resolve(null)
    return axios.get(`${ACCOUNT_API_URL}/profile/${currentUsername.value}/`, {
      headers: { Authorization: `Token ${token.value}` },
    }).then(res => {
      currentUser.value = res.data
      currentUsername.value = res.data.username
      return res.data
    }).catch(err => {
      console.error('현재 사용자 정보 fetch 실패:', err)
      throw err
    })
  }

  const updatePassword = (currentPassword, newPassword) => {
    return axios.put(`${ACCOUNT_API_URL}/password/update/`, {
      current_password: currentPassword,
      new_password: newPassword,
    }, {
      headers: { Authorization: `Token ${token.value}` },
    }).then(res => res.data)
      .catch(err => {
        const msg = err.response?.data?.detail || '비밀번호 변경 실패'
        return Promise.reject(msg)
      })
  }

    // 회원 탈퇴 API
  const deleteAccount = (password) => {
    return axios.delete(`${ACCOUNT_API_URL}/delete/`, {
      headers: { Authorization: `Token ${token.value}` },
      data: { password },
    }).then(res => res.data)
      .catch(err => {
        const msg = err.response?.data?.detail || '회원 탈퇴 실패'
        return Promise.reject(msg)
      })
  }
  // accounts.js (Pinia store)
  const fetchUserInfo = async () => {
    const res = await axios.get(`${ACCOUNT_API_URL}/user/`, {
      headers: {
        Authorization: `Token ${token.value}`,
      },
    })
    userInfo.value = res.data
  }



  return {
    ACCOUNT_API_URL,
    BOOK_API_URL,
    token,
    currentUsername,
    userInfo,
    getUserInfo,
    signUp,
    logIn,
    logOut,
    profile,
    updateProfile,
    updateInterests,
    loadSimpleBookList,
    isLogin,
    getCurrentUser,
    currentUser,
    updatePassword,
    deleteAccount,
    fetchUserInfo,
  }
}, { persist: true })
