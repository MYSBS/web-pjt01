<template>
  <div v-if="form.title" class="container py-4">
    <h2 class="mb-4 text-center">중고 책 수정</h2>

    <!-- 선택된 책 정보 -->
    <div v-if="post.book" class="mb-3 border p-3">
      <img :src="post.book.cover" class="img-fluid mb-2" style="max-height: 200px;">
      <p><strong>제목:</strong> {{ post.book.title }}</p>
      <p><strong>작가:</strong> {{ post.book.author }}</p>
    </div>

    <!-- 수정 폼 -->
    <form @submit.prevent="submitUpdate">
      <div class="mb-3">
        <label>제목</label>
        <input type="text" v-model="form.title" class="form-control" required>
      </div>

      <div class="mb-3">
        <label>내용</label>
        <textarea v-model="form.content" class="form-control" required></textarea>
      </div>

      <div class="mb-3">
        <label>이미지 (선택)</label>
        <input type="file" @change="handleFile">
      </div>

      <div class="mb-3">
        <label for="price" class="form-label">가격</label>
        <input id="price" type="number" v-model.number="form.price" class="form-control" min="0" />
      </div>

      <div class="mb-3">
        <label>판매 상태</label>
        <select v-model="form.status" class="form-select">
          <option value="판매중">판매중</option>
          <option value="판매완료">판매완료</option>
          <option value="예약중">예약중</option>
        </select>
      </div>

      <!-- 거래 위치 선택 지도 -->
      <div class="mb-3">
        <label>거래 위치</label>
        <div ref="mapSelect" class="border map-container"></div>
        <p v-if="selectedPos.lat" class="mt-2">
          선택된 위치: {{ selectedPos.lat.toFixed(5) }}, {{ selectedPos.lng.toFixed(5) }}
        </p>
      </div>

      <button type="submit" class="btn btn-primary">수정 완료</button>
    </form>
  </div>
</template>

<script setup>
import { ref, onMounted, nextTick } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useMarketStore } from '@/stores/markets'
import L from 'leaflet'
import 'leaflet/dist/leaflet.css'

const route = useRoute()
const router = useRouter()
const marketStore = useMarketStore()
const marketId = route.params.marketId

const post = ref(null)
const form = ref({
  title: '',
  content: '',
  status: '판매중',
  price: 0,
  image: null,
})
const selectedPos = ref({ lat: null, lng: null })
const mapSelect = ref(null)
let map = null
let marker = null

const handleFile = (e) => {
  form.value.image = e.target.files[0]
}

const submitUpdate = async () => {
  if (!selectedPos.value.lat) return alert('거래 위치를 선택해주세요.')

  const fd = new FormData()
  fd.append('title', form.value.title)
  fd.append('content', form.value.content)
  fd.append('status', form.value.status)
  fd.append('price', form.value.price)
  fd.append('book_id', post.value.book_id || post.value.book?.id || post.value.book?.pk)
  fd.append('latitude', selectedPos.value.lat)
  fd.append('longitude', selectedPos.value.lng)
  if (form.value.image) fd.append('image', form.value.image)

  await marketStore.updateMarketPost(marketId, fd)
  router.push({ name: 'MarketDetailView', params: { marketId } })
}

onMounted(async () => {
  const data = await marketStore.fetchMarketPost(marketId)
  post.value = data
  form.value.title = data.title
  form.value.content = data.content
  form.value.status = data.status
  form.value.price = data.price

  const defaultCoords = data.latitude && data.longitude
    ? { lat: data.latitude, lng: data.longitude }
    : { lat: 37.5665, lng: 126.9780 }
  selectedPos.value = { ...defaultCoords }

  await nextTick()  // DOM이 렌더링 된 후에
  map = L.map(mapSelect.value).setView([defaultCoords.lat, defaultCoords.lng], 13)
  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '© OpenStreetMap'
  }).addTo(map)

  marker = L.marker([defaultCoords.lat, defaultCoords.lng]).addTo(map)
    .bindPopup('거래 위치').openPopup()

  map.on('click', (e) => {
    const { lat, lng } = e.latlng
    selectedPos.value = { lat, lng }
    if (marker) marker.remove()
    marker = L.marker([lat, lng]).addTo(map)
      .bindPopup('거래 위치').openPopup()
  })

  // 렌더링 후 사이즈 재계산
  setTimeout(() => map.invalidateSize(), 0)
})
</script>

<style scoped>
textarea { resize: none; min-height: 100px }
.map-container {
  height: 300px;
  width: 100%;
  border-radius: 8px;
  overflow: hidden;
  margin-top: 0.5rem;
}
</style>