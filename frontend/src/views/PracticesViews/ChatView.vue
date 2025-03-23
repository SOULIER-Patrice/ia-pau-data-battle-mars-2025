<script setup lang="ts">
// Components
import SidePannel from '@/components/SidePannel.vue'
import SvgIcon from '@jamescoyle/vue-icon'
import { mdiMenu } from '@mdi/js'

import { ref } from 'vue'

const isOpen = ref(true)

const togglePanel = () => {
  isOpen.value = !isOpen.value
}
</script>

<template>
  <div class="chat-view">
    <SvgIcon type="mdi" :path="mdiMenu" @click="togglePanel" class="menu-button" />
    <SidePannel :isOpen="isOpen">
      <div>
        <h2>Chat</h2>
        <p>Chat with your friends</p>
      </div>
    </SidePannel>
  </div>
</template>

<style lang="scss" scoped>
.chat-view {
  display: flex;

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
}
</style>
