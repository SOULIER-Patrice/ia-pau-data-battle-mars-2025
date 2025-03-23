<script setup lang="ts">
defineProps({
  text: String,
  color: String,
  bgColor: String,
})

const emit = defineEmits(['click'])

const onClick = () => {
  emit('click')
}
</script>

<template>
  <button @click="onClick" class="button" :style="{ color: color, backgroundColor: bgColor }">
    {{ text }}
  </button>
</template>

<style lang="scss" scoped>
button {
  padding: 5px 15px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  font-weight: bold;
}
</style>
