<script setup lang="ts">
import { ref, computed, watch } from 'vue'
import { useRoute } from 'vue-router'
import SidePannel from '@/components/SidePannel.vue'
import BasicButton from '@/components/Buttons/BasicButton.vue'
import InputChatField from '@/components/Fields/InputChatField.vue'
import SvgIcon from '@jamescoyle/vue-icon'
import { mdiMenu, mdiTagOutline } from '@mdi/js'

const route = useRoute()
const isOpen = ref(true)
const chatVisible = ref(false)
const showResults = ref(false)
const selectedAnswers = ref<string[]>([])

const togglePanel = () => {
  isOpen.value = !isOpen.value
}

const toggleSubmit = () => {
  checkAnswers()
  chatVisible.value = true
}

const checkAnswers = () => {
  showResults.value = true
}

const categories = computed(() => ['Category 1', 'Category 2', 'Category 3'])
const question = 'Question ?'
const answers = ['Choice 1', 'Choice 2', 'Choice 3', 'Choice 4']
const correctAnswer = 'Choice 1'
const messages = [
  'Hello',
  'Hi',
  'How are you?',
  "I'm good",
  'What are you doing?',
  "I'm working",
  'Ok',
  'Bye',
  'Goodbye',
  'Hello',
  'Hi',
  'How are you?',
  "I'm good",
  'What are you doing?',
  "I'm working",
  'Ok',
  'Bye',
  'Goodbye',
]

// Determine if the current view is a quiz or chat based on the route
const isQuiz = computed(() => route.name === 'quiz')
</script>

<template>
  <div class="chat-quiz-view">
    <SvgIcon type="mdi" :path="mdiMenu" @click="togglePanel" class="menu-button" />
    <SidePannel :isOpen="isOpen" />
    <div :class="['floating-header', { 'is-open': isOpen }]">
      <h1>Book 1</h1>
      <BasicButton
        v-for="category in categories"
        :key="category"
        :text="category"
        :icon="mdiTagOutline"
        :iconSize="16"
        bgColor="var(--primary-color)"
        color="var(--secondary-text-color)"
      />
    </div>

    <div :class="['chat-container', { 'is-open': isOpen }]">
      <div class="scroll">
        <h1>{{ question }}</h1>

        <!-- Quiz Section -->
        <div v-if="isQuiz" class="answers">
          <div
            v-for="(answer, index) in answers"
            :key="index"
            :class="{
              'correct-answer': showResults && answer === correctAnswer,
              'wrong-answer':
                showResults && answer !== correctAnswer && selectedAnswers.includes(answer),
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
        <div v-if="!isQuiz || chatVisible" class="chat">
          <div class="message" v-for="(message, index) in messages" :key="index">
            {{ message }}
          </div>
        </div>
      </div>

      <!-- Input Field for Chat -->
      <InputChatField
        v-if="!isQuiz || chatVisible"
        placeholder="Type a message..."
        class="inputChat"
        :is-messages="messages.length > 0"
      />
    </div>
  </div>
</template>

<style lang="scss" scoped>
.chat-quiz-view {
  display: flex;
  width: 100%;

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
      display: flex;
      flex-direction: column;
      align-items: center;
      width: 100%;
      height: 100%;
      overflow: auto;
    }

    h1 {
      text-align: center;
      font-size: 32px;
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
      padding: 10px;
      margin: 5px;
      border-radius: 5px;
      width: calc(100% - 30px);
      background-color: #f1f1f1;
    }
  }

  .answers {
    display: flex;
    flex-direction: column;
    align-items: flex-start;

    input[type='checkbox'] {
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
