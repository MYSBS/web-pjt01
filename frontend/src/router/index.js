// src/router/index.js
import { createRouter, createWebHistory } from 'vue-router'
import { useAccountStore } from '@/stores/accounts'

import Homeview from '@/views/HomeView.vue'
import ThreadWriteView from '@/views/ThreadWriteView.vue'
import ThreadsListView from '@/views/ThreadsListView.vue'
import LandingView from '@/views/LandingView.vue'
import BooksListView from '@/views/BooksListView.vue'
import BookDetailView from '@/views/BookDetailView.vue'
import ThreadDetailView from '@/views/ThreadDetailView.vue'
import SignUpView from '@/views/AccountViews/SignUpView.vue'
import LogInView from '@/views/AccountViews/LogInView.vue'
import ProfileView from '@/views/AccountViews/ProfileView.vue'
import ProfileUpdateView from '@/views/AccountViews/ProfileUpdateView.vue'
import InterestSettingView from '@/views/AccountViews/InterestSettingView.vue'
import RecommendBookView from '@/views/RecommendBookView.vue'
import MarketListView from '@/views/MarketViews/MarketListView.vue'
import MarketUpdateView from '@/views/MarketViews/MarketUpdateView.vue'
import MarketCreateView from '@/views/MarketViews/MarketCreateView.vue'
import MarketDetailView from '@/views/MarketViews/MarketDetailView.vue'

// 에러페이지
const Error404 = () => import('@/views/ErrorViews/Error404.vue')
const Error500 = () => import('@/views/ErrorViews/Error500.vue')


const routes = [
  // ─────────── 공용 페이지 ───────────
  { path: '/landing',            name: 'landing',        component: LandingView },
  { path: '/accounts/login',     name: 'login',          component: LogInView },
  { path: '/accounts/signup',    name: 'signup',         component: SignUpView },

  // ─────────── 로그인 필요 ───────────
  {
    path: '/',
    name: 'main',
    component: Homeview,
    meta: { requiresAuth: true },
  },
  {
    path: '/books',
    name: 'books',
    component: BooksListView,
    meta: { requiresAuth: true },
  },
  {
    path: '/books/:bookId',
    name: 'bookDetail',
    component: BookDetailView,
    meta: { requiresAuth: true },
  },
  {
    path: '/threads/:bookId/write',
    name: 'thread-write',
    component: ThreadWriteView,
    meta: { requiresAuth: true },
  },
  {
    path: '/threads',
    name: 'threads',
    component: ThreadsListView,
    meta: { requiresAuth: true },
  },
  {
    path: '/threads/:threadId',
    name: 'threadDetail',
    component: ThreadDetailView,
    meta: { requiresAuth: true },
  },
  {
    path: '/recommend',
    name: 'recommend',
    component: RecommendBookView,
    meta: { requiresAuth: true },
  },
  {
    path: '/accounts/profile/:username',
    name: 'profile',
    component: ProfileView,
    meta: { requiresAuth: true },
        redirect: to => ({
      name: 'profile-interests',
      params: to.params
    }),
    children: [
      {
        path: 'interests',
        name: 'profile-interests',
        component: () => import('@/views/AccountViews/ProfileTabs/InterestsTab.vue'),
      },
      {
        path: 'activity',
        name: 'profile-activity',
        component: () => import('@/views/AccountViews/ProfileTabs/ActivityTab.vue'),
      },
      {
        path: 'market',
        name: 'profile-market',
        component: () => import('@/views/AccountViews/ProfileTabs/MarketTab.vue'),
      },
    ],
  },
  {
    path: '/accounts/profile/update',
    name: 'profileUpdate',
    component: ProfileUpdateView,
    meta: { requiresAuth: true },
  },
  {
    path: '/accounts/interest-setting',
    name: 'interestSetting',
    component: InterestSettingView,
    meta: { requiresAuth: true },
  },
  {
    path: '/markets',
    name: 'MarketListView',
    component: MarketListView,
    meta: { requiresAuth: true },
  },
  {
    path: '/markets/create',
    name: 'MarketCreateView',
    component: MarketCreateView,
    meta: { requiresAuth: true },
  },
  {
    path: '/markets/:marketId/update',
    name: 'MarketUpdateView',
    component: MarketUpdateView,
    meta: { requiresAuth: true },
  },
  {
    path: '/markets/:marketId',
    name: 'MarketDetailView',
    component: MarketDetailView,
    meta: { requiresAuth: true },
  },

  {
    path: '/error',
    name: 'GenericError',
    component: Error500,
    props: route => ({ message: route.params.message }),
  },
  {
    path: '/:pathMatch(.*)*',  // catch-all (404)
    name: 'GenericError',
    component: Error404,
  },
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
})

// ─── 글로벌 가드 적용 ───
// 1) Pinia store 사용 예시
router.beforeEach((to) => {
  const accountStore = useAccountStore()

  if (to.meta.requiresAuth && !accountStore.isLogin) {
    return { name: 'landing' }
  }
  if (to.name === 'landing' && accountStore.isLogin) {
    return { name: 'main' }
  }

  return true
})

// ─── 라우터 import/로드 에러 핸들링 ───
router.onError((error) => {
  console.error('[RouterError]', error)
  // 에러 페이지로 이동 (에러 메시지를 쿼리나 params로 넘길 수 있음)
  router.push({ name: 'GenericError', params: { message: error.message } })
})

export default router
