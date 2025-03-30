<script setup lang="ts">
import router from '@/router'
import type { Book } from '@/types/Book'
import SvgIcon from '@jamescoyle/vue-icon'
import { mdiNotebook, mdiFileDocumentOutline, mdiBookOpenVariantOutline } from '@mdi/js'
import SpinnerLoader from './Loaders/SpinnerLoader.vue'
import { computed, ref, watch } from 'vue'

import { useAuthStore } from '@/stores/authStore'
import type { Page } from '@/types/Page'
const authStore = useAuthStore()

const props = defineProps({
  isOpen: Boolean,
  currentBook: Object as () => Book | null,
})

const apiUrl = import.meta.env.VITE_BASE_API_URL
const selectedBook = ref<Book | null>(props.currentBook ?? null)

const books = ref<Book[]>([])
const isLoadingBooks = ref(false)
const isLoadingPages = ref(false)
const isLoading = computed(() => isLoadingBooks.value || isLoadingPages.value)

const fetchBooks = async () => {
  const userId = authStore.user?.id
  if (!userId) return

  isLoadingBooks.value = true

  fetch(`${apiUrl}/books/${userId}`, {
    headers: {
      Authorization: `Bearer ${authStore.token?.access_token}`,
    },
  })
    .then((res) => res.json())
    .then((data) => {
      books.value = data
      // Reverse the order of books
      books.value = books.value.reverse()
    })
    .catch((err) => console.error(err))
    .finally(() => {
      isLoadingBooks.value = false
    })
}
fetchBooks()

const pages = ref<Page[]>([])

const fetchPages = async (bookId: string) => {
  const userId = authStore.user?.id
  if (!userId) return

  isLoadingPages.value = true

  fetch(`${apiUrl}/books/pages/${bookId}/${userId}`, {
    headers: {
      Authorization: `Bearer ${authStore.token?.access_token}`,
    },
  })
    .then((res) => res.json())
    .then((data) => {
      pages.value = data
    })
    .catch((err) => console.error(err))
    .finally(() => {
      isLoadingPages.value = false
    })
}

watch(selectedBook, (book) => {
  pages.value = []
  if (book) {
    fetchPages(book.id)
  }
})

// Calculate font size based on text length
const calculateFontSize = (length: number): string => {
  const maxFontSize = 16 // Maximum font size in px
  const minFontSize = 10 // Minimum font size in px
  const maxLength = 200 // Maximum length for scaling

  if (length <= maxLength) {
    return `${maxFontSize - (length / maxLength) * (maxFontSize - minFontSize)}px`
  }
  return `${minFontSize}px`
}
</script>

<template>
  <div class="side-panel" :class="{ open: isOpen }">
    <div class="header">
      <div
        @click="
          () => {
            selectedBook = null
          }
        "
      >
        Books
      </div>
      <div
        @click="
          () => {
            selectedBook = props.currentBook ?? null
          }
        "
      >
        Pages
      </div>
    </div>

    <div class="content">
      <div v-if="isLoading" class="loader">
        <SpinnerLoader />
      </div>
      <div v-if="selectedBook === null">
        <div v-for="book in books" :key="book.title" @click="selectedBook = book" class="item">
          <SvgIcon
            type="mdi"
            :path="currentBook?.id === book.id ? mdiBookOpenVariantOutline : mdiNotebook"
          />
          <div :style="{ fontSize: calculateFontSize(book.title.length) }">
            {{ book.title.slice(0, 200) }}{{ book.title.length > 200 ? '...' : '' }}
          </div>
        </div>
      </div>
      <div v-else>
        <div
          v-if="selectedBook"
          v-for="page in pages || []"
          :key="page.title"
          @click="router.push(`/practice/${selectedBook.type}?page=${page.id}`)"
          class="item"
        >
          <SvgIcon type="mdi" :path="mdiFileDocumentOutline" />
          <div :style="{ fontSize: calculateFontSize(page.title.length) }">
            {{ page.title.slice(0, 200) }}{{ page.title.length > 200 ? '...' : '' }}
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style lang="scss" scoped>
/* Container styles */
.side-panel {
  position: fixed;
  padding-left: 10px;
  padding-top: 50px;
  left: -300px; /* Hidden by default */
  top: 60px;
  width: 290px;
  height: calc(100vh - (60px + 50px)); /* Header + top padding */
  background-color: #f4f3f3;
  box-shadow: 2px 0 5px rgba(0, 0, 0, 0.2);
  transition: transform 0.3s ease-in-out;
  transform: translateX(0);
  z-index: 1000;

  .header {
    display: flex;
    justify-content: space-around;
    gap: 10px;
    padding: 10px;
    margin-right: 10px;
    border-bottom: 2px solid #000;

    div {
      cursor: pointer;
    }
  }

  .content {
    overflow-y: auto;
    height: calc(100% - 50px); /* Adjust for header height */

    .loader {
      margin: 0 auto;
      margin-top: 20px;
    }

    .item {
      display: flex;
      align-items: center;
      gap: 10px;
      padding: 10px;
      cursor: pointer;

      & svg {
        width: 32px;
        height: 32px;
      }

      & div {
        width: 100%;
      }

      &:hover {
        background-color: #e0e0e0;
      }
    }
  }
}

.side-panel.open {
  transform: translateX(300px); /* Slide in */
}
</style>
