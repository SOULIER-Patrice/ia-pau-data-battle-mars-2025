<script setup lang="ts">
// Componenents
import ActiveButton from './ActiveButton.vue'

// Router
import router from '@/router'

// Props
defineProps({
  text: String,
  color: {
    type: String,
    default: 'black',
  },
  bgColor: {
    type: String,
    default: 'transparent',
  },
  activeColor: {
    type: String,
    default: 'var(--secondary-text-color)',
  },
  activeBgColor: {
    type: String,
    default: 'var(--primary-color)',
  },
  isActive: Boolean,
  to: {
    type: String,
    required: true,
  },
})
</script>

<template>
  <ActiveButton
    :text="text"
    :color="color"
    :bgColor="bgColor"
    :activeColor="activeColor"
    :activeBgColor="activeBgColor"
    :isActive="isActive"
    @click="router.push(to)"
  />
</template>

<style lang="scss" scoped></style>
