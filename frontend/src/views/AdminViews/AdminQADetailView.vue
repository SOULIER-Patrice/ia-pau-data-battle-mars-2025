<script setup lang="ts">
// Components
import QuestionForm from '@/components/Forms/QAForm.vue'
import type { QA } from '@/types/QA'
import { ref, watch } from 'vue'

// Stores
import { useAuthStore } from '@/stores/authStore'
import { useRoute } from 'vue-router'
const authStore = useAuthStore()

const qa = ref<QA | null>(null)
const isLoading = ref(false)

const base_url = import.meta.env.VITE_BASE_API_URL
const questionId = useRoute().params.id

const fetchQuestion = async (id: string) => {
  isLoading.value = true
  try {
    const response = await fetch(`${base_url}/qa/${id}`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${authStore.token?.access_token}`,
      },
    })
    if (!response.ok) {
      throw new Error('Failed to fetch question')
    }
    qa.value = await response.json()
  } catch (error) {
    console.error(error)
  } finally {
    isLoading.value = false
  }
}

watch(
  () => questionId,
  (newId) => {
    if (newId) {
      fetchQuestion(newId as string)
    }
  },
  { immediate: true },
)

const updateQuestion = async (question: QA) => {
  isLoading.value = true
  try {
    const response = await fetch(`${base_url}/qa`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${authStore.token?.access_token}`,
      },
      body: JSON.stringify(question),
    })
    if (!response.ok) {
      throw new Error('Failed to update question')
    }
    qa.value = await response.json()
  } catch (error) {
    console.error(error)
  } finally {
    isLoading.value = false
  }
}
</script>

<template>
  <div class="admin-qa-detail-view">
    <h1>Edit Question</h1>
    <QuestionForm :qa="qa" v-if="qa" @update-question="updateQuestion" />
  </div>
</template>

<style scoped lang="scss">
.admin-qa-detail-view {
  width: 100%;
  margin-top: 50px;
  display: flex;
  flex-direction: column;
  align-items: center;

  h1 {
    font-size: 48px;
    font-weight: bold;
    margin-bottom: 20px;
  }
}
</style>
