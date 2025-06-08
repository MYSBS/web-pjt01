<template>
  <div v-if="profileInfo" class="profile-container">
    <!-- 상단 정보 -->
    <div id="profile-name" class="centered-section">
      <div v-if="isMine">
        <h1>내 프로필</h1>
        <div class="button-group">
          <RouterLink :to="{ name: 'profileUpdate' }">
            <button class="edit-btn">프로필 수정</button>
          </RouterLink>
          <RouterLink :to="{ name: 'interestSetting' }">
            <button class="edit-btn">관심 설정하기</button>
          </RouterLink>
        </div>
      </div>
      <div v-else>
        <h1>{{ profileInfo.username }}의 프로필</h1>
      </div>
    </div>
    <hr />

    <!-- 프로필 이미지 -->
    <div class="centered-section">
      <img 
        v-if="profileInfo.profile_img"
        :src="profileInfo.profile_img"
        alt="프로필 이미지"
        class="profile-img"
        @error="handleImageError"
      >
      <img 
        v-else 
        :src="defaultProfileImg"
        alt="프로필 이미지(기본)"
        class="profile-img"
      >
    </div>
    <hr />

    <!-- 팔로우 정보 -->
    <div id="follow-info">
      <p>팔로워 : {{ profileInfo.follower_count }}</p>
      <p>팔로잉 : {{ profileInfo.following_count }}</p>
      <div v-if="!isMine">
        <button class="follow-btn" @click="followBnt">
          {{ isFollow ? '팔로우 취소' : '팔로우' }}
        </button>
      </div>
    </div>
    <hr />

    <!-- 탭 버튼 -->
    <div class="tab-buttons">
      <RouterLink
        :to="{ name: 'profile-interests', params: { username } }"
        class="tab-btn"
        :class="{ active: $route.name === 'profile-interests' }"
      >관심</RouterLink>

      <RouterLink
        :to="{ name: 'profile-activity', params: { username } }"
        class="tab-btn"
        :class="{ active: $route.name === 'profile-activity' }"
      >활동</RouterLink>

      <RouterLink
        :to="{ name: 'profile-market', params: { username } }"
        class="tab-btn"
        :class="{ active: $route.name === 'profile-market' }"
      >마켓활동</RouterLink>
    </div>

    <!-- 탭 내용 -->
    <hr />
    <div class="tab-content-wrapper">
      <router-view :authorTrimmer="authorTrimmer" />
    </div>

    <!-- 회원 탈퇴 버튼 -->
     <br>
    <div v-if="isMine" class="button-group">
      <button class="delete-account-btn" @click="confirmDelete">회원 탈퇴</button>
    </div>

    <!-- 비밀번호 입력 모달 -->
    <div v-if="showPasswordInput" class="modal-overlay">
      <div class="modal-box">
        <h3>비밀번호를 입력해주세요</h3>
        <input type="password" v-model="deletePassword" placeholder="비밀번호" />
        <div class="modal-buttons">
          <button @click="submitDelete">탈퇴하기</button>
          <button @click="cancelDelete">취소</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import axios from 'axios'
import { useAccountStore } from '@/stores/accounts'

const route = useRoute()
const router = useRouter()
const accountStore = useAccountStore()

const ACCOUNT_API_URL = accountStore.ACCOUNT_API_URL
const BOOK_API_URL = accountStore.BOOK_API_URL

const username = computed(() => route.params.username)
const profileInfo = computed(() => accountStore.userInfo)
const isMine = computed(() => accountStore.currentUsername === username.value)
const isFollow = ref(false)
const showPasswordInput = ref(false)
const deletePassword = ref('')
const defaultProfileImg = `${BOOK_API_URL.replace('/api/v1', '')}/static/img/user_profile/default.png`

const getFollowInfo = () => {
  accountStore.getUserInfo(username.value)
    .then((user) => {
      isFollow.value = user.is_followed
    })
    .catch(err => console.error('프로필 fetch 실패:', err))
}

const followBnt = () => {
  const csrftoken = document.cookie.split('; ').find(row => row.startsWith('csrftoken='))?.split('=')[1]

  axios({
    method: 'post',
    url: `${ACCOUNT_API_URL}/profile/${profileInfo.value.id}/follow/`,
    headers: {
      Authorization: `Token ${accountStore.token}`,
      'X-CSRFToken': csrftoken,
    },
    withCredentials: true,
  })
    .then((res) => {
      isFollow.value = res.data.is_follow
      accountStore.getUserInfo(username.value)
    })
    .catch((err) => {
      console.error('팔로우 요청 실패:', err)
    })
}

const handleImageError = (event) => {
  event.target.src = defaultProfileImg
}

const authorTrimmer = (name) => {
  if (!name) return ''
  const commaIdx = name.indexOf(',')
  const parenIdx = name.indexOf('(')

  if (commaIdx === -1 && parenIdx === -1) return name
  if (commaIdx === -1) return name.slice(0, parenIdx).trim()
  if (parenIdx === -1) return name.slice(0, commaIdx).trim()

  return name.slice(0, Math.min(commaIdx, parenIdx)).trim()
}

const confirmDelete = () => {
  showPasswordInput.value = true
}
const cancelDelete = () => {
  deletePassword.value = ''
  showPasswordInput.value = false
}
const submitDelete = () => {
  if (!deletePassword.value) {
    alert('비밀번호를 입력해주세요.')
    return
  }
  if (confirm('정말 탈퇴하시겠습니까?')) {
    accountStore.deleteAccount(deletePassword.value)
      .then((res) => {
        alert(res.detail)
        accountStore.logOut()
        router.push({ name: 'main' })
      })
      .catch((errMsg) => {
        alert(errMsg)
      })
      .finally(() => {
        deletePassword.value = ''
        showPasswordInput.value = false
      })
  }
}

onMounted(() => {
  getFollowInfo()
})

watch(() => route.params.username, (newVal, oldVal) => {
  if (newVal !== oldVal) {
    getFollowInfo()
  }
})
</script>


<style scoped>
.profile-container {
  max-width: 960px;
  margin: 4rem auto;
  padding: 2rem 1rem;
  font-family: 'Pretendard', sans-serif;
  animation: fadeIn 0.8s ease-in-out;
}

.centered-section {
  text-align: center;
}

.button-group {
  display: flex;
  justify-content: center;
  flex-wrap: wrap;
  gap: 1rem;
  margin-bottom: 2rem;
}

#profile-name h1 {
  font-size: 2rem;
  margin-bottom: 1rem;
  color: #333;
}

.profile-img {
  width: 120px;
  height: 120px;
  border-radius: 50%;
  object-fit: cover;
  margin: 1.5rem 0;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
}

.edit-btn,
.follow-btn,
.delete-account-btn {
  background-color: #6c63ff;
  color: white;
  border: none;
  padding: 0.6rem 1.4rem;
  border-radius: 30px;
  cursor: pointer;
  font-weight: 600;
  font-size: 0.95rem;
  transition: background-color 0.3s;
}

.edit-btn:hover,
.follow-btn:hover,
.delete-account-btn:hover {
  background-color: #584ff2;
}

#follow-info {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-bottom: 1rem;
}

#follow-info p {
  margin: 0.2rem 0;
  color: #444;
}

.tab-buttons {
  display: flex;
  gap: 1rem;
  justify-content: center;
  margin: 1.5rem 0;
}

.tab-btn {
  background-color: #eee;
  border: none;
  padding: 0.6rem 1.2rem;
  border-radius: 30px;
  text-decoration: none;
  color: #333;
  font-weight: 500;
  transition: all 0.3s ease;
}
.tab-btn:hover {
  background-color: #ddd;
}
.tab-btn.active {
  background-color: #6c63ff;
  color: white;
}

.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.4);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 999;
}

.modal-box {
  background: white;
  padding: 1.5rem;
  border-radius: 12px;
  box-shadow: 0 0 20px rgba(0, 0, 0, 0.1);
  width: 320px;
  text-align: center;
}
.modal-box h3 {
  margin-bottom: 1rem;
  color: #222;
}
.modal-box input {
  margin-top: 1rem;
  padding: 0.5rem;
  width: 90%;
  border: 1px solid #ccc;
  border-radius: 6px;
}
.modal-buttons {
  margin-top: 1.2rem;
  display: flex;
  justify-content: space-between;
}
.modal-buttons button {
  flex: 1;
  margin: 0 0.4rem;
  padding: 0.5rem 0;
  border-radius: 20px;
  border: none;
  background-color: #6c63ff;
  color: white;
  font-weight: 500;
  transition: background-color 0.3s;
}
.modal-buttons button:hover {
  background-color: #584ff2;
}

hr {
  margin: 2rem auto;
  width: 90%;
  border: none;
  border-top: 1px solid #ddd;
}

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
.tab-content-wrapper {
  max-width: 750px;
  margin: 0 auto;
  padding: 1rem 1.5rem;
  background-color: #fdfdfd;
  border-radius: 12px;
}
</style>
