<template>
  <header>
    <nav class="navbar navbar-expand-md bg-white border-bottom px-3 py-2">
      <!-- 왼쪽: 로고 -->
      <RouterLink to="/" class="navbar-brand">
        <img src="@/assets/images/logo.png" alt="로고" height="40" />
      </RouterLink>

      <!-- 모바일 오른쪽: 추천받기 or 로그인 + 햄버거 -->
      <div class="d-md-none ms-auto d-flex align-items-center gap-2">
        <template v-if="!accountStore.token">
          <RouterLink :to="{ name: 'login' }" class="btn-auth" @click="closeMenu">로그인</RouterLink>
        </template>
        <template v-else>
          <RouterLink :to="{ name: 'recommend' }" class="btn-recommend" @click="closeMenu">추천받기</RouterLink>
        </template>
        <button
          class="navbar-toggler"
          type="button"
          data-bs-toggle="collapse"
          data-bs-target="#navCollapse"
        >
          <span class="navbar-toggler-icon"></span>
        </button>
      </div>

      <!-- 펼쳐진 메뉴 -->
      <div class="collapse navbar-collapse justify-content-end" id="navCollapse">
        <ul class="navbar-nav gap-3">
          <li class="nav-item">
            <RouterLink :to="{ name: 'main' }" class="nav-link" @click="closeMenu">Main</RouterLink>
          </li>
          <li class="nav-item">
            <RouterLink :to="{ name: 'books' }" class="nav-link" @click="closeMenu">Books</RouterLink>
          </li>
          <li class="nav-item">
            <RouterLink :to="{ name: 'threads' }" class="nav-link" @click="closeMenu">Threads</RouterLink>
          </li>
          <li class="nav-item">
            <RouterLink :to="{ name: 'MarketListView' }" class="nav-link" @click="closeMenu">마켓</RouterLink>
          </li>

          <template v-if="!accountStore.token">
            <li class="nav-item">
              <RouterLink :to="{ name: 'login' }" class="nav-link" @click="closeMenu">로그인</RouterLink>
            </li>
            <li class="nav-item">
              <RouterLink :to="{ name: 'signup' }" class="nav-link" @click="closeMenu">회원가입</RouterLink>
            </li>
          </template>

          <template v-else>
            <li class="nav-item">
              <RouterLink :to="{ name: 'recommend' }" class="nav-link text-recommend fw-semibold" @click="closeMenu">추천받기</RouterLink>
            </li>
            <li class="nav-item">
              <button class="btn btn-outline-dark btn-sm" @click.prevent="goToProfile">내 프로필</button>
            </li>
            <li class="nav-item">
              <button class="btn btn-outline-dark btn-sm" @click.prevent="logOut">로그아웃</button>
            </li>
          </template>
        </ul>
      </div>
    </nav>
    <RouterView />
  </header>
</template>

<script setup>
import { RouterLink, RouterView, useRouter } from 'vue-router'
import { useAccountStore } from '@/stores/accounts.js'
import { nextTick } from 'vue'

const router = useRouter()
const accountStore = useAccountStore()

const logOut = function () {
  accountStore.logOut()
}

const goToProfile = () => {
  if (accountStore.currentUsername) {
    router.push({ name: 'profile', params: { username: accountStore.currentUsername } })
  } else {
    alert('로그인이 필요합니다.')
  }
}

const closeMenu = async () => {
  await nextTick()
  const navbar = document.getElementById('navCollapse')
  if (!navbar || !window.bootstrap?.Collapse) return

  if (navbar.classList.contains('show')) {
    const collapseInstance = new window.bootstrap.Collapse(navbar, {
      toggle: false
    })
    collapseInstance.hide()
  }
}
</script>

<style scoped>
.nav-link {
  color: #333;
  transition: color 0.3s;
  text-decoration: none;
  font-weight: 500;
}
.nav-link:hover {
  color: #6c63ff;
}
.text-recommend {
  color: #6c63ff;
}
.btn-recommend {
  padding: 0.4rem 1.1rem;
  border: 1px solid #6c63ff;
  background: none;
  color: #6c63ff;
  font-size: 0.95rem;
  font-weight: 500;
  letter-spacing: 0.5px;
  border-radius: 20px;
  transition: all 0.3s ease;
  text-decoration: none;
  display: inline-block;
}
.btn-recommend:hover {
  background-color: #6c63ff;
  color: #fff;
  border-color: #6c63ff;
}
.btn-auth {
  padding: 0.4rem 1rem;
  border: 1px solid #6c63ff;
  background: none;
  border-radius: 20px;
  font-size: 0.9rem;
  color: #6c63ff;
  transition: all 0.3s ease;
  text-decoration: none;
}
.btn-auth:hover {
  background-color: #6c63ff;
  color: #fff;
}
</style>
