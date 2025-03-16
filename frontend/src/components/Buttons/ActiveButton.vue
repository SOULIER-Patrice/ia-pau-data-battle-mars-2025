<script setup lang="ts">
// Components
import BasicButton from '@/components/Buttons/BasicButton.vue'

const props = defineProps<{
  text: string
  color: string
  bgColor: string
  activeColor: string
  activeBgColor: string
  isActive: boolean
}>()

const emit = defineEmits(['click'])

const onClick = () => {
  emit('click')
}
</script>

<template>
  <BasicButton
    @click="onClick"
    :text="props.text"
    :color="props.color"
    :bg-color="props.bgColor"
    :style="{
      color: props.isActive ? props.activeColor : props.color,
      backgroundColor: props.isActive ? props.activeBgColor : props.bgColor,
    }"
  />
</template>

<style lang="scss" scoped></style>
