<script setup lang="ts">
import router from '@/router'
import type { Book } from '@/types/Book'
import SvgIcon from '@jamescoyle/vue-icon'
import { mdiNotebook, mdiFileDocumentOutline } from '@mdi/js'
import { ref } from 'vue'

defineProps({
  isOpen: Boolean,
})

const selectedBook = ref<Book | null>(null)

const books = [
  {
    id: 'a67d1b1e-1b1e-4b1e-8b1e-1b1e1b1e1b1e',
    title: 'Book 1',
    type: 'quiz',
    pages: [
      {
        id: 'a67d1b1e-1b1e-4b1e-8b1e-1b1e1b1e1b1d',
        title: 'Page 1',
      },
      {
        id: 'a67d1b1e-1b1e-4b1e-8b1e-1b1e2b1e1b1d',
        title: 'Page 2',
      },
      {
        id: 'a67d1b1e-1b1e-4b3e-8b1e-1b1e1b1e1b1d',
        title: 'Page 3',
      },
    ],
  },
  {
    id: 'a67d1b1e-1b1e-4b1e-8b1e-1b1e1b1e1b1f',
    title: 'Book 2',
    type: 'chat',
    pages: [
      {
        id: 'a67d1b1e-1b1e-4b1e-8b1e-1b1e1b1e1b1d',
        title: 'Page 1',
      },
      {
        id: 'a67d1b1e-1b1e-4b1e-8b1e-1b1e2b1e1b1d',
        title: 'Page 2',
      },
      {
        id: 'a67d1b1e-1b1e-4b3e-8b1e-1b1e1b1e1b1d',
        title: 'Page 3',
      },
    ],
  },
  {
    id: 'a67d1b1e-1b1e-4b1e-8b1e-1b1e1b1e1b1a',
    title: 'Book 3',
    type: 'quiz',
    pages: [
      {
        id: 'a67d1b1e-1b1e-4b1e-8b1e-1b1e1b1e1b1d',
        title: 'Page 1',
      },
      {
        id: 'a67d1b1e-1b1e-4b1e-8b1e-1b1e2b1e1b1d',
        title: 'Page 2',
      },
      {
        id: 'a67d1b1e-1b1e-4b3e-8b1e-1b1e1b1e1b1d',
        title: 'Page 3',
      },
    ],
  },
]
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
      <div>Pages</div>
    </div>
    <div class="content">
      <div v-if="selectedBook === null">
        <div v-for="book in books" :key="book.title" @click="selectedBook = book" class="item">
          <SvgIcon type="mdi" :path="mdiNotebook" />
          <div>
            {{ book.title }}
          </div>
        </div>
      </div>
      <div v-else>
        <div
          v-if="selectedBook"
          v-for="page in selectedBook.pages || []"
          :key="page.title"
          @click="router.push(`/practice/${selectedBook.type}?page=${page.id}`)"
          class="item"
        >
          <SvgIcon type="mdi" :path="mdiFileDocumentOutline" />
          <div>
            {{ page.title }}
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
  width: 290px;
  height: 100%;
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
    .item {
      display: flex;
      align-items: center;
      gap: 10px;
      padding: 10px;
      cursor: pointer;

      &:hover {
        background-color: #f1f1f1;
      }
    }
  }
}

.side-panel.open {
  transform: translateX(300px); /* Slide in */
}
</style>
