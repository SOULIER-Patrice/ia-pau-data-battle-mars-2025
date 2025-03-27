<script setup lang="ts">
import { ref, computed, watch } from 'vue'
import { useRoute } from 'vue-router'
import SidePannel from '@/components/SidePannel.vue'
import BasicButton from '@/components/Buttons/BasicButton.vue'
import InputChatField from '@/components/Fields/InputChatField.vue'
import SvgIcon from '@jamescoyle/vue-icon'
import { mdiMenu, mdiTagOutline, mdiChevronLeft, mdiChevronRight } from '@mdi/js'

import { useAuthStore } from '@/stores/authStore'
import type { Page } from '@/types/Page'
import type { Book } from '@/types/Book'
import { marked } from 'marked'
import router from '@/router'
const authStore = useAuthStore()

const apiUrl = import.meta.env.VITE_BASE_API_URL

const route = useRoute()
const isOpen = ref(true)
const chatVisible = ref(false)
const showResults = ref(false)
const selectedAnswers = ref<string[]>([])
const answer = ref<string>('')

const togglePanel = () => {
  isOpen.value = !isOpen.value
}

const toggleSubmit = () => {
  checkAnswers()
  sendMessageQuiz()
  chatVisible.value = true
}

const checkAnswers = () => {
  showResults.value = true
}

const page = ref<Page | null>(null)
const book = ref<Book | null>(null)
const pages = ref<Page[]>([])

const fetchPage = async () => {
  const pageId = route.query.page
  const userId = authStore.user?.id

  fetch(`${apiUrl}/books/page/${pageId}/${userId}`, {
    headers: {
      Authorization: `Bearer ${authStore.token?.access_token}`,
    },
  })
    .then((res) => res.json())
    .then((data) => {
      page.value = data
      fetchBook()
      fetchPages()
    })
    .catch((err) => console.error(err))
}

watch(() => route.params.page, fetchPage, { immediate: true })

const fetchBook = async () => {
  const bookId = page.value?.book_id
  const userId = authStore.user?.id

  fetch(`${apiUrl}/books/${bookId}/${userId}`, {
    headers: {
      Authorization: `Bearer ${authStore.token?.access_token}`,
    },
  })
    .then((res) => res.json())
    .then((data) => {
      book.value = data
    })
    .catch((err) => console.error(err))
}

const fetchPages = async () => {
  const userId = authStore.user?.id
  const bookId = page.value?.book_id

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
}

const sendMessage = async (pageId: string, message: string) => {
  const userId = authStore.user?.id

  if (!userId) {
    console.error('User ID is missing')
    return
  }

  page.value?.history.push({
    user: message,
  })

  try {
    const response = await fetch(`${apiUrl}/books/send_meessage`, {
      method: 'POST',
      headers: {
        Authorization: `Bearer ${authStore.token?.access_token}`,
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        page_id: pageId,
        message,
        user_id: userId,
      }),
    })

    if (!response.ok) {
      throw new Error(`Failed to send message: ${response.statusText}`)
    }

    const data = await response.json()
    page.value?.history.push({
      ai: data,
    })
  } catch (error) {
    console.error('Error sending message:', error)
  }
}

const sendChatMessage = () => {
  if (!answer.value) return
  if (!page.value?.id) return

  sendMessage(page.value?.id, answer.value)
  answer.value = ''
}

const sendMessageQuiz = () => {
  if (!selectedAnswers.value.length) return
  if (!page.value?.id) return

  sendMessage(page.value?.id, selectedAnswers.value.join(', '))
  selectedAnswers.value = []
}

// Determine if the current view is a quiz or chat based on the route
const isQuiz = computed(() => route.name === 'MCQ')

const renderMarkdown = (markdown: string | undefined) => {
  if (!markdown) return ''
  return marked(markdown, { breaks: true })
}

//#region :    --- Navigate between pages
const currentPageIndex = computed(() => pages.value.findIndex((p) => p.id === page.value?.id))

const isFirstPage = computed(() => currentPageIndex.value === 0)
const isLastPage = computed(() => currentPageIndex.value === pages.value.length - 1)

const goToPreviousPage = () => {
  if (isFirstPage.value || !book.value) return
  const previousPage = pages.value[currentPageIndex.value - 1]
  if (previousPage) {
    router.push(`/practice/${book.value.type}?page=${previousPage.id}`)
  }
}

const goToNextPage = async () => {
  if (!book.value) return

  if (isLastPage.value) {
    const userId = authStore.user?.id
    const bookId = page.value?.book_id
    if (!userId || !bookId) return

    try {
      const response = await fetch(`${apiUrl}/books/page/${bookId}/${userId}`, {
        method: 'PUT',
        headers: {
          Authorization: `Bearer ${authStore.token?.access_token}`,
        },
      })

      if (!response.ok) {
        throw new Error(`Failed to complete book: ${response.statusText}`)
      }

      const nextPage: Page = await response.json()

      router.push(`/practice/${book.value.type}?page=${nextPage.id}`)
    } catch (error) {
      console.error('Error completing book:', error)
    }
  } else {
    const nextPage = pages.value[currentPageIndex.value + 1]
    if (nextPage) {
      router.push(`/practice/${book.value.type}?page=${nextPage.id}`)
    }
  }
}

//#endregion : --- Navigate between pages
</script>

<template>
  <div class="chat-quiz-view">
    <SvgIcon type="mdi" :path="mdiMenu" @click="togglePanel" class="menu-button" />
    <SidePannel :isOpen="isOpen" />
    <div :class="['floating-header', { 'is-open': isOpen }]">
      <h1>{{ book?.title }}</h1>
      <BasicButton
        v-for="category in book?.categories"
        :key="category"
        :text="category"
        :icon="mdiTagOutline"
        :iconSize="16"
        bgColor="var(--primary-color)"
        color="var(--secondary-text-color)"
      />
    </div>

    <SvgIcon
      type="mdi"
      :path="mdiChevronLeft"
      @click="goToPreviousPage"
      :size="64"
      :class="['chevron', 'chevron-left', { disabled: isFirstPage }, { 'is-open': isOpen }]"
    />
    <SvgIcon
      type="mdi"
      :path="mdiChevronRight"
      @click="goToNextPage"
      :size="64"
      :class="['chevron', 'chevron-right']"
    />

    <div :class="['chat-container', { 'is-open': isOpen }]">
      <div class="scroll">
        <div class="content-scroll">
          <h1>{{ page?.question }}</h1>

          <!-- Quiz Section -->
          <div v-if="isQuiz" class="answers">
            <div>
              <div
                v-for="(answer, index) in page?.options"
                :key="index"
                :class="{
                  'correct-answer': showResults && answer === page?.answer,
                  'wrong-answer':
                    showResults && answer !== page?.answer && selectedAnswers.includes(answer),
                }"
              >
                <input
                  type="checkbox"
                  :id="'answer-' + index"
                  :value="answer"
                  v-model="selectedAnswers"
                  :disabled="showResults"
                />
                <label :for="'answer-' + index">{{ answer }}</label>
              </div>
            </div>
            <BasicButton
              v-if="!showResults"
              text="Submit"
              bgColor="var(--primary-color)"
              color="var(--secondary-text-color)"
              @click="toggleSubmit"
              class="submit-button"
            />
          </div>

          <!-- Chat Section -->
          <div
            class="message"
            v-for="(message, index) in page?.history"
            :key="index"
            :class="{
              'ai-message': message.ai,
              'user-message': message.user,
            }"
          >
            <div v-html="renderMarkdown(message.ai || message.user)"></div>
          </div>
        </div>
      </div>

      <!-- Input Field for Chat -->
      <InputChatField
        v-if="!isQuiz || chatVisible"
        v-model="answer"
        @submit="sendChatMessage"
        placeholder="Type a message..."
        class="inputChat"
        :is-messages="!!(page && page.history && page.history.length > 0)"
      />
    </div>
  </div>
</template>

<style lang="scss" scoped>
.chat-quiz-view {
  display: flex;
  width: 100%;
  padding: 0 20px;

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

  .floating-header {
    display: flex;
    align-items: center;
    position: fixed;
    top: 85px;
    left: 50px;
    width: 100%;
    padding: 10px;
    transition: transform 0.3s ease-in-out;
    transform: translateX(0);
    z-index: 1000;

    h1 {
      margin: 0;
    }

    .button {
      margin: 5px;
      padding: 5px 10px;
      font-size: 10px;
    }

    &.is-open {
      transform: translateX(255px);
    }
  }

  .chevron {
    position: fixed;
    top: 50%;
    cursor: pointer;
    z-index: 1010;

    &.chevron-left {
      left: 10px;
      transition: transform 0.3s ease-in-out;

      &.is-open {
        transform: translateX(280px);
      }
    }

    &.chevron-right {
      right: 10px;
    }

    &.disabled {
      opacity: 0.5;
      cursor: not-allowed;
    }
  }

  .chat-container {
    display: flex;
    flex-direction: column;
    align-items: center;
    width: 100%;
    height: calc(100vh - 180px);
    margin-top: 70px;
    margin-bottom: 10px;
    transition:
      transform 0.3s ease-in-out,
      width 0.3s ease-in-out;
    z-index: 1000;

    .scroll {
      overflow: auto;
      width: 100%;
      height: 100%;
      display: flex;
      justify-content: center;
      align-items: center;

      .content-scroll {
        display: flex;
        flex-direction: column;
        align-items: center;
        padding: 20px;
        max-width: 700px;
        width: 100%;
        height: 100%;
      }
    }

    h1 {
      text-align: justify;
      font-size: 28px;
      margin-bottom: 10px;
    }

    &.is-open {
      width: calc(100% - 300px);
      transform: translateX(300px);
    }

    .chat {
      display: flex;
      flex-direction: column;
      align-items: flex-start;
      width: 450px;
      margin: 10px 0;
    }

    .message {
      font-weight: normal;
      padding: 10px;
      margin: 5px;
      width: calc(100% - 30px);

      &.ai-message {
        align-self: flex-start;
      }

      &.user-message {
        width: 300px;
        border-radius: 5px;
        background-color: #f4f3f3;
        align-self: flex-end;
      }
    }

    .inputChat {
      margin-top: 30px;
    }
  }

  .answers {
    display: flex;
    flex-direction: column;
    align-items: center;

    & > div {
      display: flex;
      flex-direction: column;
      align-items: flex-start;
      width: 500px;
    }

    .submit-button {
      margin-top: 10px;
      font-size: 16px;
    }

    input[type='checkbox'] {
      flex-shrink: 0;
      appearance: none;
      width: 20px;
      height: 20px;
      border: 2px solid black;
      border-radius: 50%;
      margin-right: 10px;
      cursor: pointer;
      transition:
        background-color 0.3s,
        border-color 0.3s;

      &:checked {
        background-color: var(--primary-color);
        border-color: var(--primary-color);
      }

      &:hover {
        border-color: var(--secondary-color);
      }
    }

    div {
      display: flex;
      align-items: center;
      margin: 5px 0;

      &.correct-answer {
        color: green;
        font-weight: bold;
      }

      &.wrong-answer {
        color: red;
        text-decoration: line-through;
      }
    }
  }
}
</style>
