<template>
  <div v-if="post && post.user" class="container py-4">
    <h2 class="book-title-aligned mb-4">{{ post.book.title }}</h2>

    <div class="row mb-4">
      <div class="col-md-4 text-center position-relative">
        <div id="carouselImages" class="carousel slide" data-bs-ride="carousel" data-bs-interval="2000">
          <div class="carousel-inner rounded shadow-sm">
            <div class="carousel-item active">
              <img :src="post.book.cover" class="d-block w-100 carousel-image" alt="책 표지" />
            </div>
            <div class="carousel-item" v-if="post.image">
              <img :src="post.image" class="d-block w-100 carousel-image" alt="첨부 이미지" />
            </div>
          </div>
          <button class="carousel-control-prev custom-arrow" type="button" data-bs-target="#carouselImages" data-bs-slide="prev">
            <span class="arrow-text">&lt;</span>
          </button>
          <button class="carousel-control-next custom-arrow" type="button" data-bs-target="#carouselImages" data-bs-slide="next">
            <span class="arrow-text">&gt;</span>
          </button>
        </div>
      </div>

      <div class="col-md-8">
        <div class="d-flex justify-content-between align-items-center mb-2">
          <h4 class="mb-0">{{ post.title }}</h4>
          <button v-if="isLoggedIn" class="like-btn btn-sm" @click="likePost">
            {{ post.is_liked ? '좋아요 취소' : '좋아요' }} ♥ {{ post.likes_count }}
          </button>
        </div>
        <p class="text-muted">작성자: {{ post.user.username }} / {{ formatDateTime(post.created_at) }}</p>
        <p><strong>가격:</strong> {{ post.price ? post.price + '₩' : '미기재' }}</p>
        <p>{{ post.content }}</p>

        <div class="d-flex gap-2 mt-3">
          <img v-if="post.book.cover" :src="post.book.cover" class="thumbnail-image" @click="openModal(post.book.cover)" />
          <img v-if="post.image" :src="post.image" class="thumbnail-image" @click="openModal(post.image)" />
        </div>

        <div v-if="isMine" class="mt-3">
        <RouterLink
          :to="{ name: 'MarketUpdateView', params: { marketId } }"
          class="btn btn-secondary btn-sm me-2"
        >
          수정
        </RouterLink>
        <button class="btn btn-danger btn-sm" @click="remove">삭제</button>
      </div>

        <div v-if="post.latitude && post.longitude" id="map-detail" class="mb-4"></div>
      </div>
    </div>

    <div v-if="isLoggedIn" class="mb-3">
      <textarea class="comment-textarea" v-model="newComment" placeholder="댓글을 입력하세요"></textarea>
      <button class="comment-submit-btn mt-2" @click="submit">댓글 작성</button>
    </div>

    <div v-for="comment in nestedComments" :key="comment.id" class="comment-block">
      <p class="mb-1">
        <strong>{{ comment.user.username }}</strong>
        <span class="text-muted">({{ formatDateTime(comment.created_at) }})</span>
      </p>
      <p class="mb-1">{{ comment.content }}</p>
      <div class="comment-buttons" v-if="isLoggedIn">
        <button class="comment-like-btn btn-sm" @click="likeComment(comment.id)">
          {{ isCommentLiked(comment) ? '좋아요 취소' : '좋아요' }} ♥ {{ comment.likes_count }}
        </button>

        <button v-if="comment.user.id === myId" class="btn btn-warning btn-sm ms-2">수정</button>

        <button v-if="comment.user.id === myId" class="btn btn-danger btn-sm ms-2" @click="removeComment(comment.id)">삭제</button>
        <button class="btn btn-secondary btn-sm ms-2" @click="toggleReply(comment.id)">답글</button>
      </div>

      <div v-if="replyFormVisibleId === comment.id" class="mt-2">
        <textarea class="comment-textarea mb-1" v-model="replyContent" placeholder="다짐글을 입력하세요"></textarea>
        <button class="comment-submit-btn" @click="submitReply(comment.id)">작성</button>
      </div>

      <div v-for="reply in comment.replies" :key="reply.id" class="comment-reply">
        <p class="mb-1">
          <strong>{{ reply.user.username }}</strong>
          <span class="text-muted">({{ formatDateTime(reply.created_at) }})</span>
        </p>
        <p class="mb-1">{{ reply.content }}</p>
        <div class="comment-buttons">
          <button class="comment-like-btn btn-sm" @click="likeComment(reply.id)">
            {{ isCommentLiked(reply) ? '좋아요 취소' : '좋아요' }} ♥ {{ reply.likes_count }}
          </button>

          <button v-if="reply.user.id === myId" class="btn btn-warning btn-sm ms-2">수정</button>

          <button v-if="reply.user.id === myId" class="btn btn-danger btn-sm ms-2" @click="removeComment(reply.id)">삭제</button>
        </div>
      </div>
    </div>

    <div v-if="showModal" class="modal-overlay" @click.self="closeModal">
      <div class="modal-content modal-small">
        <button class="btn-close position-absolute top-0 end-0 m-3" @click="closeModal"></button>
        <img :src="modalImage" alt="확대 이미지" />
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAccountStore } from '@/stores/accounts'
import { useMarketStore } from '@/stores/markets'
import L from 'leaflet'
import 'leaflet/dist/leaflet.css'

const route = useRoute()
const router = useRouter()
const marketId = route.params.marketId

const accountStore = useAccountStore()
const marketStore = useMarketStore()

const post = ref(null)
const newComment = ref('')
const replyContent = ref('')
const replyFormVisibleId = ref(null)
const modalImage = ref('')
const showModal = ref(false)

const isLoggedIn = computed(() => !!accountStore.token)
const myId = computed(() => accountStore.userInfo?.id)
const isMine = computed(() => post.value?.user?.id === myId.value)
const formatDateTime = marketStore.formatDateTime

const openModal = (url) => { modalImage.value = url; showModal.value = true }
const closeModal = () => { modalImage.value = ''; showModal.value = false }

const nestedComments = computed(() =>
  marketStore.comments
    .filter(comment => !comment.reply_to)
    .map(parent => ({
      ...parent, // 부모 댓글 그대로
      replies: marketStore.comments.filter(reply => reply.reply_to === parent.id)
    }))
)


const toggleReply = (id) => {
  replyFormVisibleId.value = replyFormVisibleId.value === id ? null : id
}

const submit = async () => {
  if (newComment.value.trim()) {
    await marketStore.submitComment(marketId, newComment.value.trim())
    newComment.value = ''
    await marketStore.fetchComments(marketId)
  }
}

const submitReply = async (parentId) => {
  if (replyContent.value.trim()) {
    await marketStore.submitComment(marketId, replyContent.value.trim(), parentId)
    replyContent.value = ''
    replyFormVisibleId.value = null
    await marketStore.fetchComments(marketId)
  }
}

const likeComment = async (id) => {
  await marketStore.toggleCommentLike(id)
  await marketStore.fetchComments(marketId)
}

const isCommentLiked = (comment) => comment.likes_users?.includes(myId.value)

const likePost = async () => {
  await marketStore.toggleMarketLike(marketId)
  post.value = await marketStore.fetchMarketPost(marketId)
}

const removeComment = (id) => marketStore.deleteComment(id)
const remove = () => {
  if (confirm('정말 삭제하시겠습니까?')) {
    marketStore.deleteMarketPost(marketId).then(() => router.push({ name: 'MarketListView' }))
  }
}



onMounted(async () => {
  post.value = await marketStore.fetchMarketPost(marketId)
  await marketStore.fetchComments(marketId)
  
  if (post.value.latitude && post.value.longitude) {
    const map = L.map('map-detail').setView([post.value.latitude, post.value.longitude], 15)
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      attribution: '© OpenStreetMap'
    }).addTo(map)
    L.marker([post.value.latitude, post.value.longitude])
      .addTo(map)
      .bindPopup('<strong>거래 위치</strong>')
      .openPopup()
  }
})
</script>

<style scoped>
* {
  font-family: 'Pretendard', sans-serif;
  box-sizing: border-box;
}

.btn {
  padding: 0.45rem 0.9rem;
  border-radius: 6px;
  font-size: 0.9rem;
  font-weight: 600;
  cursor: pointer;
  transition: background-color 0.2s ease;
  border: none;
}

.btn-primary,
.like-btn,
.comment-like-btn,
.comment-submit-btn {
  background-color: #6c63ff;
  color: white;
  border: none;
  border-radius: 6px;
  padding: 6px 14px;
  font-size: 0.9rem;
  font-weight: 600;
  cursor: pointer;
  transition: background-color 0.3s;
}

.btn-primary:hover,
.like-btn:hover,
.comment-like-btn:hover,
.comment-submit-btn:hover {
  background-color: #584ff2;
}

.btn-secondary {
  background-color: #aaa;
  color: white;
  border-radius: 6px;
}

.btn-secondary:hover {
  background-color: #888;
}

.btn-danger {
  background-color: #e74c3c;
  color: white;
  border-radius: 6px;
}

.btn-danger:hover {
  background-color: #c0392b;
}

.book-title-aligned {
  text-align: left;
  margin-left: 0.5rem;
  margin-bottom: 1.5rem;
  font-size: 1.8rem;
  font-weight: bold;
  color: #222;
}

textarea {
  resize: none;
  min-height: 80px;
  padding: 0.75rem 1rem;
  border: none;
  border-radius: 12px;
  width: 100%;
  font-size: 0.95rem;
  background-color: #f6f6f6;
  box-shadow: inset 0 1px 3px rgba(0, 0, 0, 0.05);
  transition: border 0.3s;
}

textarea:focus {
  outline: none;
  border: 2px solid #6c63ff;
  background-color: #fff;
}

.comment-block {
  background-color: #fefefe;
  border-radius: 12px;
  padding: 1rem;
  margin-bottom: 1rem;
  box-shadow: 0 0 6px rgba(0,0,0,0.05);
}

.comment-reply {
  margin-left: 2rem;
  border-left: 2px solid #eee;
  padding-left: 1rem;
  margin-top: 0.5rem;
}

.carousel-image {
  height: 300px;
  width: 100%;
  object-fit: cover;
  border-radius: 8px;
}

.custom-arrow {
  background: none;
  border: none;
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
  z-index: 10;
  width: 3rem;
  height: 3rem;
}

.carousel-control-prev.custom-arrow {
  left: 0.5rem;
}

.carousel-control-next.custom-arrow {
  right: 0.5rem;
}

.arrow-text {
  font-size: 2rem;
  font-weight: bold;
  color: white;
  text-shadow: 0 0 5px black;
}

.thumbnail-image {
  height: 60px;
  width: 60px;
  object-fit: cover;
  border-radius: 4px;
  cursor: pointer;
  border: 1px solid #ccc;
}

.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background-color: rgba(0, 0, 0, 0.7);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1050;
}

.modal-content.modal-small {
  position: relative;
  background-color: white;
  border-radius: 8px;
  padding: 1rem;
  width: 80vw;    
  height: 80vh;   
  display: flex;
  justify-content: center;
  align-items: center;
  overflow: hidden; 
}

.modal-content img {
  max-width: 100%;   
  max-height: 100%;   
  width: auto;
  height: auto;
  object-fit: contain;
  display: block;
  border-radius: 4px;
}

#map-detail {
  width: 100%;
  height: 200px;
  margin: 1rem auto;
  border-radius: 8px;
  overflow: hidden;
}
.btn-warning {
  background-color: #d4d3ea;  
  color: white;
  border-radius: 6px;
}

.btn-warning:hover {
  background-color: #554cf1;  
}



</style>
