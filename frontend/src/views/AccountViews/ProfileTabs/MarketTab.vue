 <template>
  <div class="market-container">
    <h3>마켓 활동</h3>
    <div class="market-inner">
      <div
        v-for="post in myMarketPosts"
        :key="post.id"
        class="market-card"
        @click="$router.push({ name: 'MarketDetailView', params: { marketId: post.id } })"
      >
        <img :src="post.book.cover" alt="책 이미지" class="book-cover" />
        <div class="card-text">
          <h5>{{ post.title }}</h5>
          <p>{{ post.book.title }} - {{ post.book.author }}</p>
          <p class="status">[{{ post.status }}]</p>
        </div>
      </div>
    </div>
  </div>
</template>


<script setup>

import { ref, onMounted } from 'vue'
import axios from 'axios'
import { useAccountStore } from '@/stores/accounts'
import { useMarketStore } from '@/stores/markets'

const accountStore = useAccountStore()
const marketStore = useMarketStore()
const myMarketPosts = ref([])

onMounted(() => {
  axios.get(`${marketStore.MARKET_API_URL}/`)
    .then((res) => {
      const myId = accountStore.userInfo.id
      myMarketPosts.value = res.data.filter(post => post.user.id === myId)
    })
})
</script>

<style scoped>.market-container {
  max-width: 960px;
  margin: 3rem auto;
  padding: 1rem;
  font-family: 'Pretendard', sans-serif;
}

.market-container h3 {
  font-size: 1.6rem;
  margin-bottom: 2rem;
}

/* 가운데 배치 레이아웃 - flex X */
.market-inner {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 2rem;
}

/* 카드 디자인은 그대로 */
.market-card {
  display: flex;
  align-items: center;
  padding: 1rem;
  border: 1px solid #e0e0e0;
  border-radius: 12px;
  background-color: #fff;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
  transition: transform 0.3s ease;
  cursor: pointer;
}
.market-card:hover {
  transform: translateY(-5px);
}

.book-cover {
  height: 100px;
  width: 70px;
  object-fit: cover;
  border-radius: 6px;
  margin-right: 1rem;
}

.card-text {
  flex-grow: 1;
}
.card-text h5 {
  margin: 0;
  font-size: 1rem;
  font-weight: 600;
  color: #222;
}
.card-text p {
  margin: 0.3rem 0;
  font-size: 0.9rem;
  color: #555;
}
.status {
  color: #6c63ff;
  font-weight: bold;
}

</style>
