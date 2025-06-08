<template>
  <form @submit.prevent="submitComment">
    <textarea
        v-model="inputContent"
        placeholder="댓글을 입력하세요"
        rows="3"
        class="comment-textarea"
    ></textarea>
    <button type="submit" class="btn submit" :disabled="!inputContent.trim()">
        등록
    </button>
  </form>
</template>

<script setup>
import { ref } from 'vue'
import { defineEmits } from 'vue'

const emit = defineEmits(['submit-comment'])
const inputContent = ref('')

const submitComment = function () {
  if (inputContent.value.trim()) {
  emit('submit-comment', inputContent.value.trim())
  inputContent.value = ''
  }
}
</script>

<style scoped>
.comment-textarea {
  width: 100%;
  padding: 0.5rem;
  border-radius: 4px;
  border: 1px solid #ccc;
  resize: vertical;
}
.btn.submit {
  margin-top: 0.5rem;
  padding: 0.5rem 1rem;
  background-color: #007acc;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}
.btn.submit:disabled {
  background-color: #ccc;
  cursor: not-allowed;
}
</style>