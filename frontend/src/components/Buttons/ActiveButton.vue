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
  activeColor: {
    type: String,
    default: 'var(--secondary-text-color)',
  },
  activeBgColor: {
    type: String,
    default: 'var(--primary-color)',
  },
  isActive: Boolean,
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
    :style="{
      color: isActive ? activeColor : color,
      backgroundColor: isActive ? activeBgColor : bgColor,
    }"
  />
</template>

<style lang="scss" scoped></style>
