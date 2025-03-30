<script setup lang="ts">
import { ref, computed, watch, nextTick } from 'vue'
import { useRoute } from 'vue-router'
import SidePannel from '@/components/SidePannel.vue'
import BasicButton from '@/components/Buttons/BasicButton.vue'
import InputChatField from '@/components/Fields/InputChatField.vue'
import SvgIcon from '@jamescoyle/vue-icon'
import { mdiMenu, mdiTagOutline, mdiChevronLeft, mdiChevronRight } from '@mdi/js'
import DotLoader from '@/components/Loaders/DotLoader.vue'

import { useAuthStore } from '@/stores/authStore'
import type { Page } from '@/types/Page'
import type { Book } from '@/types/Book'
import { marked } from 'marked'
import router from '@/router'
import SpinnerLoader from '@/components/Loaders/SpinnerLoader.vue'
const authStore = useAuthStore()

const apiUrl = import.meta.env.VITE_BASE_API_URL

const route = useRoute()
const isOpen = ref(true)
const chatVisible = ref(false)
const showResults = ref(false)
const selectedAnswer = ref<string>('')
const answer = ref<string>('')
const modelThinking = ref(false)
const page = ref<Page | null>(null)
const book = ref<Book | null>(null)
const pages = ref<Page[]>([])
const isQuiz = computed(() => route.name === 'MCQ')
const isLoading = ref(false)
const isNextPageLoading = ref(false)

const togglePanel = () => {
  isOpen.value = !isOpen.value
}

const toggleSubmit = () => {
  if (!selectedAnswer.value || !page.value) return
  checkAnswers()
  sendMessageStream(page.value?.id, selectedAnswer.value)
  chatVisible.value = true
}

const checkAnswers = () => {
  showResults.value = true
}

const fetchPage = async () => {
  const pageId = route.query.page
  const userId = authStore.user?.id
  const isLoading = ref(true)

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
      initializeChatVisibility()
    })
    .catch((err) => console.error(err))
    .finally(() => {
      isLoading.value = false
    })
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

const sendChatMessage = () => {
  if (!answer.value) return
  if (!page.value?.id) return

  sendMessageStream(page.value?.id, answer.value)
  answer.value = ''
}

const sendMessageStream = async (pageId: string, message: string) => {
  // Initialize the loader
  modelThinking.value = true

  const userId = authStore.user?.id
  const token = authStore.token?.access_token

  if (!userId || !token) {
    console.error('User ID or token is missing')
    return
  }

  page.value?.history.push({
    user: message,
  })

  // Pass the token as a query parameter
  // const response = await fetch(
  //   `${apiUrl}/stream/send_message_stream?page_id=${pageId}&message=${encodeURIComponent(message)}&user_id=${userId}&token=${token}`,
  // )

  const response = await fetch(`${apiUrl}/books/send_message_stream`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      Authorization: `Bearer ${token}`,
    },
    body: JSON.stringify({
      page_id: pageId,
      message,
      user_id: userId,
    }),
  })

  if (!response.ok) {
    console.error('Error sending message:', response.statusText)
    modelThinking.value = false
    return
  }

  const reader = response.body?.getReader()
  const decoder = new TextDecoder('utf-8')
  modelThinking.value = false

  if (!reader) {
    console.error('Failed to get reader from response body')
    return
  }

  let accumulatedMessage = ''

  while (true) {
    const { done, value } = await reader.read()
    if (done) break

    const chunk = decoder.decode(value, { stream: true })
    const lines = chunk.split('[END_CHUNK]\n\n')

    for (const line of lines) {
      try {
        // Supposons que chaque ligne commence par "data: "
        if (line.startsWith('data: ')) {
          const data = line.substring(6) // Retire "data: "
          accumulatedMessage += data

          // Mettez à jour l'interface utilisateur de manière réactive
          // Supprimez uniquement le dernier message de l'IA s'il existe
          if (
            page.value?.history &&
            page.value?.history.length > 0 &&
            'ai' in page.value?.history[page.value?.history.length - 1]
          ) {
            page.value?.history.pop()
          }
          page.value?.history.push({
            ai: accumulatedMessage,
          })
        }
      } catch (error) {
        console.error('Error parsing data:', error, line)
      }
    }
  }
  reader.releaseLock()
}

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

    isNextPageLoading.value = true

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
    } finally {
      isNextPageLoading.value = false
    }
  } else {
    const nextPage = pages.value[currentPageIndex.value + 1]
    if (nextPage) {
      router.push(`/practice/${book.value.type}?page=${nextPage.id}`)
    }
  }
}

//#endregion : --- Navigate between pages

const getAnswerClass = (index: number) => {
  switch (index) {
    case 0:
      return 'answer-a'
    case 1:
      return 'answer-b'
    case 2:
      return 'answer-c'
    case 3:
      return 'answer-d'
    default:
      return ''
  }
}

const isCorrectAnswer = (index: number) => {
  return page.value?.answer === String.fromCharCode(65 + index)
}

const isWrongAnswer = (index: number) => {
  if (!showResults.value || !page.value) return false
  return showResults.value && !isCorrectAnswer(index)
}

const initializeChatVisibility = () => {
  if (!page.value) return
  if (page.value?.history.length > 0) {
    chatVisible.value = true
    showResults.value = true
    if (isQuiz.value && page.value?.history[0].user) {
      selectedAnswer.value = page.value?.history[0].user
    }
  }
}

const shouldHideFirstMessage = (index: number) => {
  if (!page.value) return false
  return index === 0 && page.value?.history.length > 0
}
</script>

<template>
  <div class="chat-quiz-view">
    <SpinnerLoader v-if="isLoading" class="global-loader" :size="5" />
    <SvgIcon type="mdi" :path="mdiMenu" @click="togglePanel" class="menu-button" />
    <SidePannel :isOpen="isOpen" :current-book="book" class="side-pannel" />
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

    <SpinnerLoader v-if="isNextPageLoading" class="chevron chevron-right" :size="2" />
    <SvgIcon
      v-if="!isNextPageLoading"
      type="mdi"
      :path="mdiChevronRight"
      @click="goToNextPage"
      :size="64"
      :class="['chevron', 'chevron-right']"
    />

    <div :class="['chat-container', { 'is-open': isOpen }]">
      <div class="scroll">
        <div class="content-scroll">
          <div v-html="renderMarkdown('Question: ' + page?.question)"></div>

          <!-- Quiz Section -->
          <div v-if="isQuiz" class="answers">
            <div>
              <div
                v-for="(answer, index) in page?.options"
                :key="index"
                :class="[
                  'answer-option',
                  getAnswerClass(index),
                  {
                    'correct-answer': showResults && isCorrectAnswer(index),
                    'wrong-answer': showResults && isWrongAnswer(index),
                  },
                ]"
              >
                <input
                  type="radio"
                  :id="'answer-' + index"
                  :value="answer"
                  v-model="selectedAnswer"
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

          <!-- Answer of the user before true answer for free response -->
          <div class="message user-message" v-if="page && !isQuiz && page?.history.length > 0">
            <div v-html="renderMarkdown(page.history[0].user)"></div>
          </div>

          <!-- True answer for free response -->
          <div class="message" v-if="page && !isQuiz && page?.history.length > 0">
            <div v-html="renderMarkdown('Answer: ' + page.answer)"></div>
          </div>

          <!-- Justification for quiz -->
          <div class="message" v-if="page && isQuiz && showResults">
            <div v-html="renderMarkdown('Justification: ' + page.justification)"></div>
          </div>

          <!-- Chat Section -->
          <div
            v-for="(message, index) in page?.history"
            :key="index"
            class="message"
            :class="{
              'ai-message': message.ai,
              'user-message': message.user,
              hidden: shouldHideFirstMessage(index),
            }"
          >
            <div v-html="renderMarkdown(message.ai || message.user)"></div>
          </div>
          <!-- Loader -->
          <DotLoader v-if="modelThinking" class="message chat-loader" />
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
  flex-direction: column;
  width: 100%;
  padding: 0 20px;

  .global-loader {
    position: fixed;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    z-index: 1000;
  }

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
    top: 75px;
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

    .message {
      font-weight: normal;
      padding: 10px;
      margin: 5px;

      &.ai-message {
        align-self: flex-start;
      }

      &.user-message {
        width: 300px;
        border-radius: 5px;
        background-color: #f4f3f3;
        align-self: flex-end;
      }

      &.chat-loader {
        align-self: flex-start;
        margin: 0 15px;
        width: 20px;
      }

      &.hidden {
        display: none;
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
      padding: 10px 20px;
    }

    .answer-option {
      width: 100%;
    }

    .submit-button {
      margin-top: 10px;
      font-size: 16px;
    }

    input[type='radio'] {
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
