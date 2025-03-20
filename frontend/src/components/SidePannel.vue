<script setup lang="ts">
defineProps({
  isOpen: Boolean,
})
</script>

<template>
  <div class="side-panel" :class="{ open: isOpen }">
    <slot></slot>
  </div>
</template>

<style lang="scss" scoped>
/* Container styles */
.side-panel {
  position: fixed;
  padding-left: 10px;
  padding-top: 50px;
  left: -300px; /* Hidden by default */
  width: 290px;
  height: 100%;
  background-color: #fff;
  box-shadow: 2px 0 5px rgba(0, 0, 0, 0.2);
  transition: transform 0.3s ease-in-out;
  transform: translateX(0);
  z-index: 1000;
}

.side-panel.open {
  transform: translateX(300px); /* Slide in */
}
</style>
