<template>
  <div class="modal-overlay" @click.self="close">
    <div class="modal-box">
      <h2 class="modal-title">비밀번호 변경</h2>
      
      <div class="form-group">
        <label for="currentPassword">현재 비밀번호</label>
        <input
          id="currentPassword"
          v-model="currentPassword"
          type="password"
          placeholder="현재 비밀번호 입력"
        />
      </div>

      <div class="form-group">
        <label for="newPassword">새 비밀번호</label>
        <input
          id="newPassword"
          v-model="newPassword"
          type="password"
          placeholder="새 비밀번호 입력"
        />
      </div>

      <div class="button-group">
        <button class="btn cancel" @click="close">취소</button>
        <button class="btn confirm" @click="submit">변경하기</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useAccountStore } from '@/stores/accounts'

const emit = defineEmits(['close', 'success'])
const currentPassword = ref('')
const newPassword = ref('')
const accountStore = useAccountStore()

const submit = () => {
  accountStore.updatePassword(currentPassword.value, newPassword.value)
    .then(res => {
      alert(res.detail)
      emit('success')
    })
    .catch(errMsg => {
      alert(errMsg)
    })
}

const close = () => emit('close')
</script>

<style scoped>
.modal-overlay {
  position: fixed;
  inset: 0;
  background-color: rgba(0, 0, 0, 0.4);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 999;
}

.modal-box {
  background: #fff;
  width: 90%;
  max-width: 400px;
  padding: 2rem;
  border-radius: 12px;
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.15);
  animation: fadeIn 0.2s ease-in-out;
}

.modal-title {
  font-size: 1.5rem;
  font-weight: bold;
  margin-bottom: 1.5rem;
  text-align: center;
  color: #6c63ff;
}

.form-group {
  margin-bottom: 1rem;
}

.form-group label {
  display: block;
  font-weight: 600;
  margin-bottom: 0.5rem;
  color: #333;
}

.form-group input {
  width: 100%;
  padding: 0.6rem;
  border: 1px solid #ccc;
  border-radius: 8px;
  font-size: 1rem;
  transition: border-color 0.3s;
}

.form-group input:focus {
  border-color: #6c63ff;
  outline: none;
}

.button-group {
  display: flex;
  justify-content: flex-end;
  gap: 0.8rem;
  margin-top: 1.5rem;
}

.btn {
  padding: 0.6rem 1.2rem;
  border: none;
  border-radius: 8px;
  font-size: 1rem;
  cursor: pointer;
}

.btn.cancel {
  background-color: #e0e0e0;
  color: #333;
}

.btn.cancel:hover {
  background-color: #ccc;
}

.btn.confirm {
  background-color: #6c63ff;
  color: #fff;
}

.btn.confirm:hover {
  background-color: #594be2;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(-10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
</style>
