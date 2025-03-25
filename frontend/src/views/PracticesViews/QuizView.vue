<script setup lang="ts">
import { ref, computed } from 'vue'
import SidePannel from '@/components/SidePannel.vue'
import BasicButton from '@/components/Buttons/BasicButton.vue'
import InputChatField from '@/components/Fields/InputChatField.vue'
import SvgIcon from '@jamescoyle/vue-icon'
import { mdiMenu, mdiTagOutline } from '@mdi/js'

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
</script>

<template>
  <div class="chat-view">
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
        <div class="answers">
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
        </div>
        <button @click="toggleSubmit" class="submit-button">Submit</button>
        <div v-if="chatVisible" class="chat">
          <div class="message">Hello</div>
          <div class="message">Hi</div>
          <div class="message">How are you?</div>
          <div class="message">I'm good</div>
          <div class="message">What are you doing?</div>
          <div class="message">I'm working</div>
          <div class="message">Ok</div>
          <div class="message">Bye</div>
          <div class="message">Hello</div>
          <div class="message">lo</div>
          <div class="message">How are you?</div>
          <div class="message">I'm good</div>
          <div class="message">What are you doing?</div>
          <div class="message">I'm working</div>
          <div class="message">Ok</div>
          <div class="message">Bye</div>
        </div>
      </div>
      <InputChatField placeholder="Type a message..." class="inputChat" v-if="chatVisible" />
    </div>
  </div>
</template>

<style lang="scss" scoped>
.chat-view {
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
    background-color: #dbd8cf;
    z-index: 1000;
    top: 85px;
    left: 50px;
    width: 100%;
    padding: 10px;
    transition: transform 0.3s ease-in-out;
    transform: translateX(0);

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
    height: calc(100vh - 280px);
    margin-top: 70px;
    margin-bottom: 10px;
    padding-bottom: 80px;
    transition:
      transform 0.3s ease-in-out,
      width 0.3s ease-in-out;

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

    .answers {
      display: flex;
      flex-direction: column;
      align-items: flex-start;

      div {
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

    .submit-button,
    .request-explanation-button {
      margin: 10px;
      padding: 10px 20px;
      background-color: var(--primary-color);
      color: white;
      border: none;
      border-radius: 5px;
      cursor: pointer;

      &:hover {
        background-color: var(--primary-color);
      }
    }

    .chat {
      padding: 10px;
      height: calc(100% - 50px);
    }

    .message {
      padding: 10px;
      margin: 5px;
      border-radius: 5px;
      width: 300px;
      background-color: #f1f1f1;
    }
  }

  .inputChat {
    position: absolute;
    bottom: 0;
    margin: auto;
  }
}
</style>
