<template>
  <div id="app">
    <!-- 네비게이션 -->
    <header class="navbar-container">
      <nav class="navbar-inner">
        <!-- 로고 -->
        <RouterLink to="/" class="logo">README</RouterLink>

        <!-- 햄버거 버튼 (모바일 전용) -->
        <button class="hamburger d-md-none" @click="toggleMenu">
          ☰
        </button>

        <!-- 네비 메뉴 -->
        <ul :class="['nav-menu', { open: isMenuOpen }]">
          <template v-if="accountStore.isLogin">
            <li><RouterLink to="/" class="nav-link">홈</RouterLink></li>
            <li><RouterLink to="/books" class="nav-link">북</RouterLink></li>
            <li><RouterLink to="/threads" class="nav-link">포스트</RouterLink></li>
            <li><RouterLink to="/markets" class="nav-link nav-highlight">마켓</RouterLink></li>
            <li><RouterLink to="/recommend" class="btn-recommend">추천받기</RouterLink></li>
            <li><button class="nav-button" @click="goToProfile">내프로필</button></li>
            <li><button class="nav-button" @click="logOut">로그아웃</button></li>
          </template>
          <template v-else>
            <li><RouterLink to="/accounts/login" class="nav-link">로그인</RouterLink></li>
            <li><RouterLink to="/accounts/signup" class="nav-link">회원가입</RouterLink></li>
          </template>
        </ul>
      </nav>
    </header>



    <!-- 본문 -->
    <main class="page-container">
      <RouterView />
    </main>
  </div>
</template>

<script setup>
  import { RouterLink, RouterView, useRoute, useRouter } from 'vue-router'
  import { useAccountStore } from '@/stores/accounts.js'
  import { computed, ref } from 'vue'

  const route = useRoute()
  const router = useRouter()
  const accountStore = useAccountStore()

  const isLanding = computed(() => route.name === 'landing')

  const logOut = () => {
    accountStore.logOut()
    router.push({ name: 'landing' })
  }

  const goToProfile = () => {
    if (accountStore.currentUsername) {
      router.push({ name: 'profile', params: { username: accountStore.currentUsername } })
    } else {
      alert('로그인이 필요합니다.')
    }
  }

  const isMenuOpen = ref(false)
  const toggleMenu = () => {
    isMenuOpen.value = !isMenuOpen.value
  }

</script>

<style scoped>

/* 전체 네비 컨테이너 */
.navbar-container {
  width: 100%;
  background-color: #ffffff;
  display: flex;
  justify-content: center;
  border-bottom: 1px solid #eee;
}

/* 내부 네비 정렬 (로고 + 메뉴 + 햄버거) */
.navbar-inner {
  width: 100%;
  max-width: 1100px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 1rem 1.5rem;
  flex-wrap: wrap;
  position: relative;
}

/* 로고 */
.logo {
  font-weight: bold;
  font-size: 1.5rem;
  color: #6c63ff;
  text-decoration: none;
}

/* 햄버거 버튼 (모바일 전용) */
.hamburger {
  font-size: 1.8rem;
  background: none;
  border: none;
  color: #333;
  cursor: pointer;
  margin-left: auto;
  display: none; /* 기본은 숨김 */
}

/* 메뉴 리스트 */
.nav-menu {
  list-style: none;
  display: flex;
  align-items: center;
  gap: 1.4rem;
  margin: 0;
  padding-left: 0;
  flex-wrap: wrap;
  transition: max-height 0.3s ease, padding-top 0.3s ease;
}

/* 메뉴 항목 링크 */
.nav-link {
  color: #333;
  text-decoration: none;
  font-weight: 500;
  transition: color 0.3s;
}
.nav-link:hover {
  color: #6c63ff;
}

/* 포인트 강조 링크 (마켓 등) */
.nav-highlight {
  color: #6c63ff;
  font-weight: 600;
}

/* 추천받기 버튼 스타일 */
.btn-recommend {
  background-color: #6c63ff;
  color: white !important;
  padding: 0.5rem 1.1rem;
  border-radius: 30px;
  font-size: 0.95rem;
  font-weight: 600;
  text-decoration: none;
  transition: background-color 0.3s;
}
.btn-recommend:hover {
  background-color: #574fd3;
}

/* 프로필/로그아웃 버튼 */
.nav-button {
  background: none;
  border: none;
  font-weight: 500;
  font-size: 0.95rem;
  cursor: pointer;
  color: #333;
  transition: color 0.3s;
}
.nav-button:hover {
  color: #6c63ff;
}

@media (max-width: 768px) {
  .hamburger {
    display: block;
    z-index: 1001;
  }

  .nav-menu {
    position: absolute;
    top: 100%;
    right: 1.5rem;
    background: white;
    flex-direction: column;
    align-items: flex-end;
    text-align: right;
    gap: 0.8rem;
    padding: 1rem;
    border-radius: 12px;
    box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);

    transform: scaleY(0);
    transform-origin: top;
    transition: transform 0.25s ease, opacity 0.25s ease;
    opacity: 0;
    visibility: hidden;
    z-index: 1000;
  }

  .nav-menu.open {
    transform: scaleY(1);
    opacity: 1;
    visibility: visible;
  }
}
.page-container {
  max-width: 1100px;
  margin: 0 auto;
  padding: 2rem 1.5rem;
}




</style>
