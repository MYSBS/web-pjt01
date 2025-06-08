<template>
  <div class="login-container">
    <div class="login-box">
      <h1 class="login-title">로그인</h1>

      <form @submit.prevent="logIn">
        <label for="username">아이디</label>
        <input type="text" id="username" v-model.trim="username">

        <label for="password">비밀번호</label>
        <input type="password" id="password" v-model.trim="password">

        <input type="submit" value="logIn">
      </form>

      <br>
      <p class="signup-msg">
        계정이 없으신가요?
        <RouterLink :to="{ name: 'signup' }" class="btn-signup">회원가입</RouterLink>
      </p>

    </div>
  </div>
</template>

<script setup>
  import { ref } from 'vue'
  import { useAccountStore } from '@/stores/accounts.js'
  import { useRouter } from 'vue-router'

  const accountStore = useAccountStore()
  const router = useRouter()

  const username = ref(null)
  const password = ref(null)

  const logIn = function () {
    const payload = {
      username: username.value,
      password: password.value
    }
    accountStore.logIn(payload)
      .then(() => {
        router.push({ name: 'main' })
      })
      .catch(() => {
        alert('아이디 또는 비밀번호가 잘못되었습니다. 다시 시도해주세요.')
      })
  }
</script>

<style scoped>
.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  background: linear-gradient(135deg, #ece9e6, #ffffff);
  font-family: 'Pretendard', sans-serif;
}

.login-box {
  background-color: #fff;
  padding: 3rem;
  border-radius: 20px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
  width: 100%;
  max-width: 400px;
  text-align: center;
}

.login-title {
  font-size: 2rem;
  font-weight: bold;
  margin-bottom: 2rem;
  color: #333;
}

form {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

label {
  text-align: left;
  font-size: 0.95rem;
  font-weight: 500;
  color: #444;
}

input[type="text"],
input[type="password"] {
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

input[type="submit"] {
  margin-top: 1rem;
  padding: 0.8rem 1rem;
  background-color: #6c63ff;
  color: white;
  font-size: 1rem;
  font-weight: 600;
  border: none;
  border-radius: 30px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

input[type="submit"]:hover {
  background-color: #584ff2;
}
</style>
