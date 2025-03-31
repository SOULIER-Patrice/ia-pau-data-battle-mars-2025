<script setup lang="ts">
import List from '@/components/List/List.vue'
import InputField from '@/components/Fields/InputField.vue'
import type { QA } from '@/types/QA'
import type { Item } from '@/types/Item'
import { useAuthStore } from '@/stores/authStore'
import { ref, watch, computed } from 'vue'
import SpinnerLoader from '@/components/Loaders/SpinnerLoader.vue'

const authStore = useAuthStore()

const apiUrl = import.meta.env.VITE_BASE_API_URL

const qas = ref<QA[]>([])
const isLoading = ref(false)

// Filtres
const searchQuery = ref('')
const selectedCategory = ref('')
const selectedVerification = ref('')
const selectedType = ref('')

const categories = [
  'Filing requirements and formalities',
  'Priority claims and right of priority',
  'Divisional applications',
  'Fees, payment methods, and time limits',
  'Languages and translations',
  'Procedural remedies and legal effect',
  'Pct procedure and entry into the european phase',
  'Examination, amendments, and grant',
  'Opposition and appeals',
  'Substantive patent law: novelty and inventive step',
  'Entitlement and transfers',
  'Biotech and sequence listings',
  'Unity of invention',
]

// Fonction pour transformer les données QA en Items
const transformQAToItems = (qas: QA[]): Item[] => {
  return qas.map((qa) => ({
    title: qa.question.slice(0, 100) + (qa.question.length > 100 ? '...' : ''), // Limiter la longueur de la question
    description: `${qa.type} | ${qa.categories} | ${qa.answer.slice(0, 100) + (qa.answer.length > 100 ? '...' : '')}`,
    href: `/admin/qa/${qa.id}`,
    chips: [
      {
        title: qa.is_verified ? 'Verified' : 'Not Verified',
        color: '#fff',
        bgColor: qa.is_verified ? 'var(--primary-color)' : 'var(--warning-color)',
      },
    ],
  }))
}

// Fonction pour filtrer les données QA
const filteredQas = computed(() => {
  return qas.value.filter((qa) => {
    const matchesSearch =
      qa.question.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
      qa.answer.toLowerCase().includes(searchQuery.value.toLowerCase())
    const matchesCategory =
      !selectedCategory.value || qa.categories.includes(selectedCategory.value)
    const matchesVerification =
      !selectedVerification.value ||
      (selectedVerification.value === 'Verified' && qa.is_verified) ||
      (selectedVerification.value === 'Not Verified' && !qa.is_verified)
    const matchesType = !selectedType.value || qa.type === selectedType.value

    return matchesSearch && matchesCategory && matchesVerification && matchesType
  })
})

// Items générés à partir des QAs filtrés
const filteredItems = computed(() => transformQAToItems(filteredQas.value))

// Fetch QA data
const fetchQaData = async () => {
  isLoading.value = true
  try {
    const response = await fetch(`${apiUrl}/qa`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${authStore.token?.access_token}`,
      },
    })

    if (!response.ok) {
      throw new Error('Failed to fetch QA data')
    }

    const data = await response.json()
    qas.value = data
  } catch (error) {
    console.error('Error fetching QA data:', error)
  } finally {
    isLoading.value = false
  }
}

watch(
  () => authStore.token,
  (newToken) => {
    if (newToken) {
      fetchQaData()
    }
  },
  { immediate: true },
)
</script>

<template>
  <div class="admin-qa-view">
    <h1>Admin QA Management</h1>
    <p>Manage questions and answers from this view.</p>

    <!-- Filter Container -->
    <div class="filter-container">
      <InputField label="Search" placeholder="Search by question or answer" v-model="searchQuery" />
      <select v-model="selectedCategory">
        <option value="">All Categories</option>
        <option v-for="category in categories" :key="category" :value="category">
          {{ category }}
        </option>
        <!-- Add more categories as needed -->
      </select>
      <select v-model="selectedVerification">
        <option value="">All</option>
        <option value="Verified">Verified</option>
        <option value="Not Verified">Not Verified</option>
      </select>
      <select v-model="selectedType">
        <option value="">All Types</option>
        <option value="OPEN">OPEN</option>
        <option value="MCQ">MCQ</option>
      </select>
    </div>

    <SpinnerLoader v-if="isLoading" />
    <List v-else title="Questions and Answers" :items="filteredItems" :limit="10" class="qa-list" />
    <router-link to="/admin">Back to Admin Home</router-link>
  </div>
</template>

<style scoped lang="scss">
.admin-qa-view {
  display: flex;
  width: 100%;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 20px;

  .filter-container {
    display: flex;
    flex-wrap: wrap;
    gap: 10px;
    width: 100%;
    max-width: 600px;
    margin-bottom: 20px;

    select,
    input {
      flex: 1;
      padding: 5px;
      border: 1px solid #ccc;
      border-radius: 5px;
    }
  }

  .qa-list {
    width: 100%;
    max-width: 600px;
    margin: 0 auto;
  }

  h1 {
    font-size: 64px;
    color: var(--primary-text-color);
  }

  p {
    font-size: 1rem;
    font-weight: normal;
    color: var(--primary-text-color);
  }

  a {
    font-size: 1.5rem;
    color: var(--primary-text-color);
    text-decoration: none;

    &:hover {
      text-decoration: underline;
    }
  }
}
</style>
