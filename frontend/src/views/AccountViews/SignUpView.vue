<template>
  <div class="signup-container">
    <div class="signup-box">
      <h1 class="signup-title">회원가입</h1>

      <form @submit.prevent="signUp">
        <label for="username">ID</label>
        <input type="text" id="username" v-model.trim="username">

        <label for="password1">비밀번호</label>
        <input type="password" id="password1" v-model.trim="password1">

        <label for="password2">비밀번호 재입력</label>
        <input type="password" id="password2" v-model.trim="password2">
        <p v-if="passwordMismatch" class="error-message">비밀번호가 일치하지 않습니다.</p>

        <label>성별</label>
        <div class="radio-group">
          <label><input type="radio" value="M" v-model="gender"> 남</label>
          <label><input type="radio" value="F" v-model="gender"> 여</label>
        </div>

        <label for="age">나이</label>
        <input type="number" id="age" v-model="age">

        <label for="weekly_avg_reading_time">주간 평균 독서 시간 (분)</label>
        <input type="number" id="weekly_avg_reading_time" v-model="weekly_avg_reading_time">

        <label for="annual_reading_amount">연간 독서량</label>
        <input type="number" id="annual_reading_amount" v-model="annual_reading_amount">

        <label for="profile_img">프로필 이미지</label>
        <input type="file" id="profile_img" @change="onFileChange">

        <button type="submit">회원가입</button>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useAccountStore } from '@/stores/accounts.js'

const accountStore = useAccountStore()

const username = ref('')
const password1 = ref('')
const password2 = ref('')
const gender = ref('M')
const age = ref(0)
const weekly_avg_reading_time = ref(0)
const annual_reading_amount = ref(0)
const profile_img = ref(null)
const passwordMismatch = ref(false)
const signupError = ref(false)

const onFileChange = (event) => {
  profile_img.value = event.target.files[0]
}

const signUp = async () => {
  passwordMismatch.value = (password1.value !== password2.value)
  if (passwordMismatch.value) return
  signupError.value = false

  const formData = new FormData()
  formData.append('username', username.value)
  formData.append('password1', password1.value)
  formData.append('password2', password2.value)
  formData.append('gender', gender.value)
  formData.append('age', age.value)
  formData.append('weekly_avg_reading_time', weekly_avg_reading_time.value)
  formData.append('annual_reading_amount', annual_reading_amount.value)
  if (profile_img.value) {
    formData.append('profile_img', profile_img.value)
  }

  try {
    await accountStore.signUp(formData)
  } catch (err) {
    if (err.response?.data?.username) {
      alert('사용 중인 아이디입니다.')
    } else if (err.response?.data?.password1) {
      alert('비밀번호 조건을 확인해주세요.')
    } else {
      alert('회원가입에 실패했습니다. 입력값을 확인해주세요.')
    }
    signupError.value = true
  }
}
</script>

<style scoped>
.signup-container {
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 4rem 1rem;
  background: linear-gradient(135deg, #ece9e6, #ffffff);
  min-height: 100vh;
  font-family: 'Pretendard', sans-serif;
}

.signup-box {
  background-color: #fff;
  padding: 3rem;
  border-radius: 20px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
  width: 100%;
  max-width: 500px;
}

.signup-title {
  font-size: 2rem;
  font-weight: bold;
  margin-bottom: 2rem;
  color: #333;
  text-align: center;
}

form {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

label {
  font-size: 0.95rem;
  font-weight: 500;
  color: #444;
  margin-bottom: 0.25rem;
}

input[type="text"],
input[type="password"],
input[type="number"],
input[type="file"] {
  padding: 0.75rem 1rem;
  border: 1px solid #ccc;
  border-radius: 12px;
  font-size: 1rem;
  transition: border-color 0.2s ease;
}

input:focus {
  border-color: #6c63ff;
  outline: none;
}

.radio-group {
  display: flex;
  gap: 1.5rem;
  margin-bottom: 0.5rem;
}

button[type="submit"] {
  margin-top: 1rem;
  padding: 0.9rem 1rem;
  background-color: #6c63ff;
  color: white;
  font-size: 1rem;
  font-weight: 600;
  border: none;
  border-radius: 30px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

button[type="submit"]:hover {
  background-color: #584ff2;
}

.error-message {
  color: #e53935;
  font-size: 0.9rem;
  margin-top: -0.5rem;
  margin-bottom: 0.5rem;
  text-align: left;
}
</style>