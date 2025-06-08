<template>
  <section class="comments-section">
    <h3>댓글 ({{ comments.length }})</h3>
    <br>
    <CommentForm @submit-comment="handleAdd" />
    <CommentList
      :comments="comments"
      @delete-comment="handleDelete"
      @update-comment="handleUpdate"
    />
  </section>
</template>

<script setup>
import { onMounted, computed } from 'vue'
import { useRoute } from 'vue-router'
import { useThreadStore } from '@/stores/threads'
import CommentForm from './CommentForm.vue'
import CommentList from './CommentList.vue'

const route = useRoute()
const threadStore = useThreadStore()
const threadId = Number(route.params.threadId)

onMounted(() => {
  threadStore.getThreadDetail(threadId)
})


const comments = computed(() => threadStore.threadDetail.comments || [])
const nowUser = computed(() => threadStore.threadUsername)

function handleAdd(content) {
  threadStore.createComment(threadId, { content })
}

async function handleDelete(commentId) {
  try {
    await threadStore.deleteComment(threadId, commentId)
  } catch (err) {
    console.error('댓글 삭제 실패:', err)
    alert('댓글 삭제에 실패했습니다.')
  }
}

async function handleUpdate(commentId, content) {
  try {
    await threadStore.updateComment(threadId, commentId, { content })
  } catch (err) {
    console.error('댓글 수정 실패:', err)
    alert('댓글 수정에 실패했습니다.')
  }
}
</script>

<style scoped>
.comments-section {
  margin-top: 2rem;
  padding-top: 1rem;
  border-top: 1px solid #ddd;
}
</style>
