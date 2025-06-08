<template>
  <div class="profile-update">
    <h2>프로필 수정</h2>

    <form @submit.prevent="submitUpdate">
      <div>
        <label>나이</label>
        <input type="number" v-model.number="form.age" />
      </div>
      <div>
        <label>주간 평균 독서 시간</label>
        <input type="number" v-model.number="form.weekly_avg_reading_time" />
      </div>
      <div>
        <label>연간 독서량</label>
        <input type="number" v-model.number="form.annual_reading_amount" />
      </div>
      <div>
        <label>프로필 이미지</label>
        <input type="file" @change="handleFile" />
        <div v-if="previewImage">
          <img :src="previewImage" alt="preview" width="100" />
        </div>
      </div>
      <div>
        <label>
          <input type="checkbox" v-model="resetToDefault" />
          기본 이미지로 변경
        </label>
      </div>
      <button type="submit">수정 완료</button>
    </form>
    
    <button @click="showPasswordModal = true">비밀번호 변경</button>

    <PasswordChangeModal
      v-if="showPasswordModal"
      @close="showPasswordModal = false"
      @success="onPasswordChangeSuccess"
    />

  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAccountStore } from '@/stores/accounts'
import PasswordChangeModal from '@/components/accounts/PasswordChangeModal.vue'

const router = useRouter()
const accountStore = useAccountStore()

const resetToDefault = ref(false)
const previewImage = ref(null)
const isModalOpen = ref(false)

const form = ref({
  age: '',
  weekly_avg_reading_time: '',
  annual_reading_amount: '',
  profile_img: null,
})

const handleFile = (event) => {
  const file = event.target.files[0]
  form.value.profile_img = file
  previewImage.value = URL.createObjectURL(file)
}

const submitUpdate = async () => {
  const formData = new FormData()
  formData.append('age', form.value.age)
  formData.append('weekly_avg_reading_time', form.value.weekly_avg_reading_time)
  formData.append('annual_reading_amount', form.value.annual_reading_amount)

  if (resetToDefault.value) {
    formData.append('reset_profile', 'true')
  } else if (form.value.profile_img) {
    formData.append('profile_img', form.value.profile_img)
  }

  const res = await accountStore.updateProfile(formData)
  if (res) {
    alert('프로필 수정 완료!')
    router.push({ name: 'profile', params: { username: accountStore.currentUsername } })
  } else {
    alert('프로필 수정 실패!')
  }
}

const showPasswordModal = ref(false)
const onPasswordChangeSuccess = () => {
  showPasswordModal.value = false
  alert('비밀번호 변경이 완료되었습니다.')
}

onMounted(() => {
  accountStore.getUserInfo(accountStore.currentUsername)
    .then((user) => {
      form.value.age = user.age ?? ''
      form.value.weekly_avg_reading_time = user.weekly_avg_reading_time ?? ''
      form.value.annual_reading_amount = user.annual_reading_amount ?? ''
    })
    .catch((err) => {
      console.error('기존 프로필 정보 불러오기 실패:', err)
    })
})
</script>

<style scoped>
.profile-update {
  max-width: 500px;
  margin: 0 auto;
  padding: 1rem;
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

form > div {
  margin-bottom: 1rem;
}

label {
  font-weight: bold;
  display: block;
  margin-bottom: 0.3rem;
}

input[type='number'],
input[type='password'],
input[type='file'] {
  width: 100%;
  padding: 0.5rem;
  border: 1px solid #ccc;
  border-radius: 0.3rem;
}

button {
  padding: 0.5rem 1rem;
  background-color: #444;
  color: white;
  border: none;
  border-radius: 0.3rem;
  cursor: pointer;
}

button:hover {
  background-color: #333;
}
</style>
