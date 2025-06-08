<template>
  <div class="container py-4">
    <h2 class="mb-4 text-market">중고 책 등록</h2>

    <!-- 책 검색 버튼 -->
    <button class="btn btn-outline-market mb-3" @click="showBookModal = true">
      책 선택하기
    </button>

    <!-- 선택된 책 정보 -->
    <div v-if="selectedBook" class="mb-3 border p-3">
      <img :src="selectedBook.fields.cover" class="img-fluid mb-2" style="max-height: 200px;">
      <p><strong>제목:</strong> {{ selectedBook.fields.title }}</p>
      <p><strong>작가:</strong> {{ selectedBook.fields.author }}</p>
    </div>

    <!-- 게시글 작성 폼 -->
    <form @submit.prevent="submitPost">
      <div class="mb-3">
        <label>제목</label>
        <input type="text" v-model="form.title" class="form-control">
      </div>

      <div class="mb-3">
        <label>내용</label>
        <textarea v-model="form.content" class="form-control"></textarea>
      </div>

      <div class="mb-3">
        <label>이미지 (선택)</label>
        <input type="file" @change="handleFile">
      </div>

      <div class="mb-3">
        <label for="price" class="form-label">가격</label>
        <input id="price" type="number" v-model="form.price" class="form-control" />
      </div>


      <div class="mb-3">
        <label>판매 상태</label>
        <select v-model="form.status" class="form-select">
          <option value="판매중">판매중</option>
          <option value="판매완료">판매완료</option>
          <option value="예약중">예약중</option>
        </select>
      </div>
      
      <!-- 지도에서 위치 선택 -->
      <div class="mb-3">
        <label>거래 위치 선택</label>
        <div id="map-select" class="border" style="height: 300px;"></div>
        <p v-if="selectedPos.lat" class="mt-2">
          선택된 위치: {{ selectedPos.lat.toFixed(5) }}, {{ selectedPos.lng.toFixed(5) }}
        </p>
      </div>


      <button type="submit" class="btn btn-market">저장</button>
    </form>

    <!-- 책 검색 모달 -->
    <div v-if="showBookModal" class="book-modal-wrapper" @click.self="showBookModal = false">
      <div class="book-modal bg-white shadow">

        <!-- 검색 헤더 (고정) -->
        <div class="book-modal-header p-4 border-bottom">
          <h5 class="text-market mb-3">책 검색</h5>
          <input
            type="text"
            v-model="searchTerm"
            class="form-control"
            placeholder="책 제목을 검색하세요"
          >
        </div>

        <!-- 스크롤 가능한 책 리스트 -->
        <div class="book-modal-body p-4">
          <div v-if="searchTerm && filteredBooks.length">
            <div
              v-for="book in filteredBooks"
              :key="book.pk"
              class="border p-2 mb-2 rounded"
              :class="{ 'bg-light': selectedBook?.pk === book.pk }"
              @click="selectBook(book)"
              style="cursor: pointer"
            >
              <img :src="book.fields.cover" class="me-2" style="height: 60px;">
              {{ book.fields.title }} - {{ book.fields.author }}
            </div>
          </div>

          <div v-else-if="searchTerm" class="text-muted">검색 결과가 없습니다.</div>
        </div>

        <div class="p-4 border-top text-end">
          <button class="btn btn-outline-market" @click="showBookModal = false">닫기</button>
        </div>
      </div>
    </div>

  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useMarketStore } from '@/stores/markets'
import { useBookStore } from '@/stores/book'
import L from 'leaflet'
import 'leaflet/dist/leaflet.css'

const router = useRouter()
const marketStore = useMarketStore()
const bookStore = useBookStore()

// --- 기존 refs ---
const books = ref([])
const selectedBook = ref(null)
const showBookModal = ref(false)
const searchTerm = ref('')
const form = ref({
  title: '',
  content: '',
  status: '판매중',
  image: null,
  price: 0,
})
const selectedPos = ref({ lat: null, lng: null })

// 파일 처리
const handleFile = (e) => { form.value.image = e.target.files[0] }

// 책 선택
const selectBook = (book) => {
  selectedBook.value = book
  showBookModal.value = false
}
const filteredBooks = computed(() => {
  const kw = (searchTerm.value || '').toLowerCase()
  return books.value.filter(b => b.fields.title.toLowerCase().includes(kw))
})

// 폼 제출
const submitPost = async () => {
  if (!selectedBook.value) {
    return alert('책을 선택해주세요.')
  }
  if (!selectedPos.value.lat) {
    return alert('위치를 지도에서 클릭해 선택해주세요.')
  }
  const fd = new FormData()
  fd.append('title', form.value.title)
  fd.append('content', form.value.content)
  fd.append('status', form.value.status)
  fd.append('price', form.value.price)
  fd.append('book_id', selectedBook.value.pk)
  fd.append('latitude', selectedPos.value.lat)
  fd.append('longitude', selectedPos.value.lng)
  if (form.value.image) fd.append('image', form.value.image)

  await marketStore.createMarketPost(fd)
  router.push({ name: 'MarketListView' })
}

onMounted(async () => {
  // 도서 리스트 로드
  books.value = await bookStore.getSimpleBookList()

  // 기본 위치 (서울 시청)
  const defaultCoords = { lat: 37.5665, lng: 126.9780 }

  // 지도를 생성할 요소
  const mapEl = document.getElementById('map-select')

  // 위치 얻기 & 지도 초기화 함수
  const initMap = ({ lat, lng }) => {
    const map = L.map(mapEl).setView([lat, lng], 17)
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      attribution: '© OpenStreetMap'
    }).addTo(map)

    let marker = null
    map.on('click', (e) => {
      const { lat, lng } = e.latlng
      selectedPos.value = { lat, lng }
      if (marker) marker.remove()
      marker = L.marker([lat, lng]).addTo(map)
        .bindPopup('거래 위치').openPopup()
    })
  }

  // Geolocation 사용
  if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(
      pos => {
        initMap({
          lat: pos.coords.latitude,
          lng: pos.coords.longitude
        })
      },
      _err => {
        // 거부·실패 시 기본 위치로
        initMap(defaultCoords)
      },
      { enableHighAccuracy: true, timeout: 5000 }
    )
  } else {
    // 지원 안 하면 기본 위치로
    initMap(defaultCoords)
  }
})
</script>



<style scoped>
.text-market {
  color: #6c63ff;
}

.btn-market {
  background-color: #6c63ff;
  color: white;
  border: none;
}
.btn-market:hover {
  background-color: #554dde;
}

.btn-outline-market {
  border: 1px solid #6c63ff;
  color: #6c63ff;
  background: none;
}
.btn-outline-market:hover {
  background-color: #6c63ff;
  color: white;
}

.book-modal-wrapper {
  position: fixed;
  top: 0; left: 0; right: 0; bottom: 0;
  background: rgba(0, 0, 0, 0.3);
  z-index: 1000;
  display: flex;
  justify-content: center;
  align-items: center;
}

.book-modal {
  width: 500px;
  max-height: 80vh;
  display: flex;
  flex-direction: column;
  border-radius: 8px;
  background: white;
}

.book-modal-header {
  background: white;
  position: sticky;
  top: 0;
  z-index: 10;
}

.book-modal-body {
  overflow-y: auto;
  flex-grow: 1;
  max-height: 300px; /* 3~4개 정도 보이는 높이 */
}

/* 기존 스타일 + 지도 박스 약간의 패딩 */
#map-select {
  margin-top: 0.5rem;
  border-radius: 4px;
  overflow: hidden;
}

</style>
