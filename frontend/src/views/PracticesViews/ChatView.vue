<script setup lang="ts">
// Components
import SidePannel from '@/components/SidePannel.vue'
import BasicButton from '@/components/Buttons/BasicButton.vue'
import InputChatField from '@/components/Fields/InputChatField.vue'
import SvgIcon from '@jamescoyle/vue-icon'
import { mdiMenu, mdiTagOutline } from '@mdi/js'

import { computed, ref } from 'vue'

const isOpen = ref(true)

const togglePanel = () => {
  isOpen.value = !isOpen.value
}

const categories = computed(() => ['Category 1', 'Category 2', 'Category 3'])
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
      <h1>Question ?</h1>
      <div class="chat">
        <div class="message">Hello</div>
        <div class="message">Hi</div>
        <div class="message">How are you?</div>
        <div class="message">I'm good</div>
        <div class="message">What are you doing?</div>
        <div class="message">I'm working</div>
        <div class="message">Ok</div>
        <div class="message">Bye</div>
      </div>
      <InputChatField placeholder="Type a message..." />
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
    margin-top: 70px;
    margin-bottom: 10px;
    transition:
      transform 0.3s ease-in-out,
      width 0.3s ease-in-out;
    z-index: 1000;

    h1 {
      font-size: 32px;
    }

    &.is-open {
      width: calc(100% - 300px);
      transform: translateX(300px);
    }

    .chat {
      padding: 10px;
      overflow-y: auto;
      height: calc(100% - 50px);
    }

    .message {
      padding: 10px;
      margin: 5px;
      border-radius: 5px;
      background-color: #f1f1f1;
    }
  }
}
</style>
