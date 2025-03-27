<script setup lang="ts">
// Components
import BasicCard from '@/components/Cards/BasicCard.vue'
import SvgIcon from '@jamescoyle/vue-icon'
import SidePannel from '@/components/SidePannel.vue'
import { mdiTagOutline, mdiMenu } from '@mdi/js'

import { ref } from 'vue'
import ActiveButton from '@/components/Buttons/ActiveButton.vue'

import { useAuthStore } from '@/stores/authStore'
import type { Page } from '@/types/Page'
import router from '@/router'
const authStore = useAuthStore()

const apiUrl = import.meta.env.VITE_BASE_API_URL

const isOpen = ref(false)
const togglePanel = () => {
  isOpen.value = !isOpen.value
}

const categories = [
  'Minimum requirements for a filing date',
  'Filing methods and locations',
  'Formality examination',
  'Substantive requirements for priority',
  'Time limits and restoration',
  'Multiple priorities and partial priority',
  'Filing requirements',
  'Subject-matter and scope',
  'Formality examination',
  'Types and calculation of fees',
  'Payment mechanisms',
  'Fee deadlines and late payment consequences',
  'Language of filing and procedural language',
  'Translation requirements on grant or other stages',
  'Effects of language on costs and procedural rights',
  'Further processing (rule 135 epc)',
  'Re-establishment of rights (article 122 epc)',
  'Loss of rights and remedies',
  'International filing and search',
  'Preliminary examination and amendments',
  'European phase entry and requirements',
  'Examination procedure and communications',
  'Claim amendments and article 123 epc',
  'Grant stage (rule 71(3) epc) and post-grant publication',
  'Grounds for opposition (article 100 epc)',
  'Opposition procedure and admissibility',
  'Appeal proceedings',
  'Novelty analysis',
  'Inventive step analysis',
  'Special forms of claims (e.g., medical use)',
  'Entitlement disputes (article 61 EPC)',
  'Transfers and assignments',
  'Procedural consequences',
  'Sequence listing filing and format',
  'Added subject-matter in biotech claims',
  'Specific patentability exceptions in biotech',
  'Unity of invention',
  'Unity in pct applications',
  'Strategies for overcoming lack of unity',
]
const selectedCategories = ref<string[]>([])

const toggleCategory = (category: string) => {
  if (selectedCategories.value.includes(category)) {
    selectedCategories.value = selectedCategories.value.filter((c) => c !== category)
  } else {
    selectedCategories.value = [...selectedCategories.value, category]
  }
}

const createBook = (type: string) => {
  const userId = authStore.user?.id
  if (!userId) return

  fetch(`${apiUrl}/books/create`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      Authorization: `Bearer ${authStore.token?.access_token}`,
    },
    body: JSON.stringify({
      categories: selectedCategories.value,
      type,
      user_id: userId,
    }),
  })
    .then((res) => res.json())
    .then((data: Page) => {
      router.push(`/practice/${type}?page=${data.id}`)
    })
    .catch((err) => {
      console.error(err)
    })
}

const mode = ref<string>('')
</script>

<template>
  <div class="select-mode-view">
    <SvgIcon type="mdi" :path="mdiMenu" @click="togglePanel" class="menu-button" />
    <SidePannel :isOpen="isOpen" class="side-pannel" />
    <h1>Which way to practice ?</h1>
    <div class="cards" v-if="mode === ''">
      <BasicCard title="Multiple-responses" buttonText="Choose this option" @click="mode = 'MCQ'">
        <div class="select-mode-view__content">
          <p>This category consists to choose one answer between different responses.</p>
        </div>
      </BasicCard>
      <BasicCard title="Free response" buttonText="Choose this option" @click="mode = 'chat'">
        <div class="select-mode-view__content">
          <p>This category consists to write your own answer.</p>
        </div>
      </BasicCard>
    </div>
    <div v-else>
      <BasicCard title="Choose a category" buttonText="Start" @click="() => createBook(mode)">
        <div class="select-categories__content">
          <ActiveButton
            v-for="category in categories"
            :key="category"
            :text="category"
            @click="toggleCategory(category)"
            color="var(--secondary-text-color)"
            bg-color="#444443"
            activeColor="var(--secondary-text-color)"
            activeBgColor="var(--primary-color)"
            :isActive="selectedCategories.includes(category)"
            :icon="mdiTagOutline"
          />
        </div>
      </BasicCard>
    </div>
  </div>
</template>

<style lang="scss" scoped>
.select-mode-view {
  display: flex;
  flex: 1;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  gap: 50px;

  .menu-button {
    position: fixed;
    top: 80px;
    left: 5px;
    cursor: pointer;
    margin: 10px;
    z-index: 1001;
    border-radius: 50%;
    padding: 5px;

    &:hover {
      background-color: #f4f3f3;
    }
  }

  .side-pannel {
    margin-top: 150px;
  }

  h1 {
    font-size: 64px;
    color: var(--primary-text-color);
  }

  .cards {
    display: flex;
    gap: 100px;

    .card {
      width: 400px;
      height: 300px;
    }

    .select-mode-view__content {
      p {
        font-size: 1rem;
        font-weight: normal;
        color: var(--primary-text-color);
      }
    }
  }

  .select-categories__content {
    display: flex;
    flex-wrap: wrap;
    gap: 10px;
  }
}
</style>
.
