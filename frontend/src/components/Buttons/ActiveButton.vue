<script setup lang="ts">
// Components
import BasicButton from '@/components/Buttons/BasicButton.vue'

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
  icon: {
    type: String,
    required: false,
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
  isLoading: {
    type: Boolean,
    default: false,
  },
})

const emit = defineEmits(['click'])

const onClick = () => {
  emit('click')
}
</script>

<template>
  <BasicButton
    @click="onClick"
    :text="text"
    :color="color"
    :bg-color="bgColor"
    :icon="icon"
    :isLoading="isLoading"
    :style="{
      color: isActive ? activeColor : color,
      backgroundColor: isActive ? activeBgColor : bgColor,
    }"
  />
</template>

<style lang="scss" scoped></style>
