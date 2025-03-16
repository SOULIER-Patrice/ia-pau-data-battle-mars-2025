<script setup lang="ts">
const props = defineProps<{
  text: string
  color: string
  bgColor: string
}>()

const emit = defineEmits(['click'])

const onClick = () => {
  emit('click')
}
</script>

<template>
  <button
    @click="onClick"
    class="button"
    :style="{ color: props.color, backgroundColor: props.bgColor }"
  >
    {{ text }}
  </button>
</template>

<style lang="scss" scoped>
button {
  padding: 5px 15px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}
</style>
