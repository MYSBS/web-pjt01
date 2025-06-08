<template>
  <div class="comment-item">
    <!-- 수정 모드일 때 -->
    <div v-if="isEditing" class="edit-mode">
      <textarea 
        v-model="editContent" 
        class="edit-textarea"
        rows="3"
      ></textarea>
      <div class="edit-actions">
        <button class="btn-save" @click="saveEdit">저장</button>
        <button class="btn-cancel" @click="cancelEdit">취소</button>
      </div>
    </div>
    
    <!-- 일반 보기 모드 -->
    <div v-else>
      <p class="content">{{ comment.content }}</p>
      <div class="meta">
        <span class="author">작성자 : {{ usernameData }}</span>
        <span class="created">작성시간 : {{ formattedDate }}</span>
        
        <!-- 작성자만 수정/삭제 버튼 표시 -->
        <div class="comment-actions" v-if="canDelete">
          <button class="btn-edit" @click="startEdit">수정</button>
          <button class="btn-delete" @click="confirmDelete">삭제</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useThreadStore } from '@/stores/threads'
// 실제 스토어 파일명이 account.js 라면 import 경로도 account 이어야 합니다.
import { useAccountStore } from '@/stores/accounts'

const threadStore = useThreadStore()
const accountStore = useAccountStore()

// 수정 관련 상태
const isEditing = ref(false)
const editContent = ref('')

const props = defineProps({
  comment: {
    type: Object,
    required: true,
    // 예시 타입 선언: user가 숫자 id, created_at이 ISO 문자열이라고 가정
    // user: Number,
    // created_at: String,
  }
})
const emit = defineEmits(['delete-comment'])


const usernameData = ref('')
const formattedDate = computed(() =>
  new Date(props.comment.created_at).toLocaleString()
)

// 1) 댓글 작성자 이름 불러오기
// 2) 현재 로그인 유저 정보 불러오기
onMounted(async () => {
  // (1) 댓글 작성자 username
  if (props.comment.user != null) {
    await threadStore.getCommentUsername(props.comment.user)
    usernameData.value = threadStore.commentUsername.username
  }

  // (2) 로그인 되어 있으면 currentUser fetch
  if (accountStore.isLogin) {
    await accountStore.getCurrentUser()
  }

})

// canDelete 로직: currentUser 객체에 id(pk) 프로퍼티가 무엇으로 들어오는지 확인하세요.
// 백엔드가 id 대신 pk라는 필드를 쓰는지, 아니면 id인지 보시고 그쪽으로 맞춥니다.
const canDelete = computed(() => {
  const user = accountStore.currentUser
  if (!user) return false

  // 백엔드 응답에 따라 둘 중 하나로 비교
  const userPk = user.pk ?? user.id
  return userPk === props.comment.user
})

// 수정 시작
const startEdit = () => {
  editContent.value = props.comment.content
  isEditing.value = true
}

// 수정 취소
const cancelEdit = () => {
  editContent.value = ''
  isEditing.value = false
}

// 수정 저장
const saveEdit = () => {
  if (editContent.value.trim()) {
    emit('update-comment', props.comment.id, editContent.value.trim())
    isEditing.value = false
  }
}

// 삭제 확인
const confirmDelete = () => {
  if (confirm('정말로 이 댓글을 삭제하시겠습니까?')) {
    emit('delete-comment', props.comment.id)
  }
}

</script>

<style scoped>
.comment-item {
  padding: 0.75rem;
  border-bottom: 1px solid #eee;
}

.meta {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.875rem;
  color: #666;
}

.comment-actions {
  margin-left: auto;
  display: flex;
  gap: 0.5rem;
}

.btn-edit, .btn-delete {
  background: none;
  border: none;
  cursor: pointer;
  font-size: 0.875rem;
}

.btn-edit {
  color: #007acc;
}

.btn-delete {
  color: #e74c3c;
}

.btn-edit:hover {
  text-decoration: underline;
}

.btn-delete:hover {
  text-decoration: underline;
}

.content {
  margin-top: 0.5rem;
  white-space: pre-wrap;
}

.edit-mode {
  margin-top: 0.5rem;
}

.edit-textarea {
  width: 100%;
  padding: 0.5rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  resize: vertical;
  font-family: inherit;
}

.edit-actions {
  margin-top: 0.5rem;
  display: flex;
  gap: 0.5rem;
}

.btn-save, .btn-cancel {
  padding: 0.25rem 0.75rem;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.875rem;
}

.btn-save {
  background-color: #007acc;
  color: white;
}

.btn-cancel {
  background-color: #666;
  color: white;
}

.btn-save:hover {
  background-color: #005a9e;
}

.btn-cancel:hover {
  background-color: #555;
}
</style>