<script setup lang="ts">
// Components
import BasicCard from '@/components/Cards/BasicCard.vue'
import { mdiTagOutline } from '@mdi/js'

import { ref } from 'vue'
import ActiveButton from '@/components/Buttons/ActiveButton.vue'

const categories = ['Category 1', 'Category 2', 'Category 3', 'Category 4', 'Category 5']
const selectedCategories = ref<string[]>([])

const toggleCategory = (category: string) => {
  if (selectedCategories.value.includes(category)) {
    selectedCategories.value = selectedCategories.value.filter((c) => c !== category)
  } else {
    selectedCategories.value = [...selectedCategories.value, category]
  }
}

const mode = ref<string>('')
</script>

<template>
  <div class="select-mode-view">
    <h1>Which way to practice ?</h1>
    <div class="cards" v-if="mode === ''">
      <BasicCard title="Multiple-responses" buttonText="Choose this option" @click="mode = 'quiz'">
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
      <BasicCard
        title="Choose a category"
        buttonText="Start"
        @click="() => $router.push(`/practice/${mode}?categories=${selectedCategories.join(',')}`)"
      >
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
