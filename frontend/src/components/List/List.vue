<script setup lang="ts">
import { ref, computed } from 'vue'
import ItemList from './ItemList.vue'
import BasicButton from '../Buttons/BasicButton.vue'
import type { Item } from '../../types/Item'

export type ListProps = {
  title?: string
  limit?: number
  items?: Item[] // Utilisation du type Item
}

const props = defineProps<ListProps>()

const currentPage = ref(1)

// Calculer le nombre total de pages
const totalPages = computed(() => {
  if (props.limit) {
    return Math.ceil((props.items?.length || 0) / props.limit)
  }
  return 1
})

// Calculer les indices de début et de fin pour la pagination
const startIndex = computed(
  () => (currentPage.value - 1) * (props.limit || props.items?.length || 0),
)
const endIndex = computed(() => startIndex.value + (props.limit || props.items?.length || 0))

// Extraire les items paginés
const paginatedItems = computed(() => props.items?.slice(startIndex.value, endIndex.value) || [])

// Changer la page actuelle
const setCurrentPage = (page: number) => {
  currentPage.value = page
}
</script>

<template>
  <div class="container">
    <div v-if="props.title" class="title">{{ props.title }}</div>
    <div>
      <!-- Afficher uniquement les items paginés -->
      <template v-for="(item, index) in paginatedItems" :key="index">
        <ItemList
          :title="item.title"
          :description="item.description"
          :href="item.href"
          :buttons="item.buttons"
          :chips="item.chips"
          class="item"
        />
      </template>
    </div>
    <div v-if="props.limit" class="pagination">
      <BasicButton
        text="Previous"
        @click="() => setCurrentPage(Math.max(currentPage - 1, 1))"
        :disabled="currentPage === 1"
      />
      <span>{{ currentPage }} / {{ totalPages }}</span>
      <BasicButton
        text="Next"
        @click="() => setCurrentPage(Math.min(currentPage + 1, totalPages))"
        :disabled="currentPage === totalPages"
      />
    </div>
  </div>
</template>

<style scoped>
.container {
  width: 100%;
  align-items: baseline;
}
.title {
  font-size: 20px;
  font-weight: bold;
  margin-bottom: 10px;
}
.pagination {
  width: 100%;
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 10px;
}

.item {
  margin-bottom: 10px;
}
</style>
