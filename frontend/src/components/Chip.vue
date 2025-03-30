<script setup lang="ts">
defineProps({
  title: String,
  color: String,
  bgColor: String,
})
</script>

<template>
  <div :class="['chip']" :style="{ backgroundColor: bgColor, color: color }">
    <span>{{ title }}</span>
  </div>
</template>

<style scoped lang="scss">
.chip {
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 5px 10px;
  border-radius: 5px;
  font-size: 14px;
  color: #fff; /* Default text color */
  background-color: var(--primary-color); /* Default color */
}
</style>
