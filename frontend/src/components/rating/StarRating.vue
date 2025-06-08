<template>
  <div class="star-rating">

    <!-- 보기 모드 -->
    <template v-if="!isEditing">
      <span
        v-for="star in 5"
        :key="star"
        class="star"
        :class="{
          filled: star <= current,
          'half-filled': star - 0.5 === current
        }"
      >★</span>
      <button class="edit-btn" @click="startEditing">수정</button>
    </template>

    <!-- 편집 모드 -->
    <template v-else>
      <span
        v-for="star in 5"
        :key="star"
        class="star"
        :class="{
          filled: star <= (hover || selected),
          'half-filled': star - 0.5 === (hover || selected)
        }"
        @mousemove="onMouseMove(star, $event)"
        @mouseleave="onMouseLeave"
        @click="chooseStar(star, $event)"
      >★</span>
      <button class="confirm-btn" @click="submitRating">완료</button>
    </template>

    <!-- 평균 및 내 별점 텍스트 -->
    <span class="avg-text">
      평균: {{ avg.toFixed(1) }} / 5
    </span>
    <span class="my-text">
      내 별점: {{ current.toFixed(1) }} / 5
    </span>

  </div>
</template>

<script setup>
import { ref, watch, onMounted } from 'vue'
import { useBookStore } from '@/stores/book'

const props = defineProps({
  bookId: { type: Number, required: true }
})

const store      = useBookStore()
const current    = ref(0)
const avg        = ref(0)
const hover      = ref(0)
const selected   = ref(0)
const isEditing  = ref(false)

// 평점 로딩
async function loadRatings() {
  await store.fetchBookRating(props.bookId)
  current.value  = store.userRating
  avg.value      = store.averageRating
  selected.value = store.userRating
}
onMounted(loadRatings)
watch(() => store.userRating,  loadRatings)
watch(() => store.averageRating, loadRatings)

// 편집 모드 시작
function startEditing() {
  isEditing.value = true
}

// 마우스 오버 계산
function onMouseMove(star, event) {
  const { offsetX, target } = event
  hover.value = offsetX < target.offsetWidth / 2 ? star - 0.5 : star
}
function onMouseLeave() {
  hover.value = 0
}

// 별점 선택
function chooseStar(star, event) {
  const { offsetX, target } = event
  selected.value = offsetX < target.offsetWidth / 2 ? star - 0.5 : star
}

// 편집 완료
async function submitRating() {
  await store.submitBookRating(props.bookId, selected.value)
  alert('별점이 성공적으로 등록되었습니다.')
  await loadRatings()
  isEditing.value = false
}
</script>

<style scoped>
.star {
  position: relative;
  font-size: 2rem;
  cursor: pointer;
  color: #ccc;
  user-select: none;
  display: inline-block;
}
.star.filled {
  color: #f5b301;
}
.star.half-filled::before {
  content: '★';
  position: absolute;
  left: 0;
  top: 0;
  width: 50%;
  overflow: hidden;
  color: #f5b301;
}

.edit-btn,
.confirm-btn {
  margin-left: 1rem;
  padding: 0.3rem 0.6rem;
  font-size: 1rem;
  border: 1px solid #ccc;
  background: white;
  cursor: pointer;
  border-radius: 4px;
}
.edit-btn:hover,
.confirm-btn:hover {
  background: #f5f5f5;
}

.avg-text,
.my-text {
  margin-left: 1rem;
  font-size: 1rem;
  vertical-align: middle;
}
.my-text {
  font-weight: bold;
}
</style>
