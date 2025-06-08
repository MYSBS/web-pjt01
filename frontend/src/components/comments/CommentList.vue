<template>
  <div class="comment-list">
    <CommentItem
      v-for="c in comments"
      :key="c.id"
      :comment="c"
      @delete-comment="onDeleteComment"
      @update-comment="onUpdateComment"
    />
    <p v-if="!comments.length" class="no-comments">댓글이 없습니다.</p>
  </div>
</template>

<script setup>
import { defineProps, defineEmits } from 'vue'
import CommentItem from './CommentItem.vue'

const props = defineProps({ comments: Array })
const emit = defineEmits(['delete-comment', 'update-comment'])

function onDeleteComment(id) {
  emit('delete-comment', id)
}

function onUpdateComment(id, content) {
  emit('update-comment', id, content)
}
</script>

<style scoped>
.comment-list {
  margin-top: 1rem;
}
.no-comments {
  text-align: center;
  color: #999;
}
</style>
