<script setup lang="ts">
// Components
import SvgIcon from '@jamescoyle/vue-icon'

defineProps({
  title: String,
  color: {
    type: String,
    required: false,
    default: 'var(--primary-color)',
  },
  bgColor: {
    type: String,
    required: false,
    default: 'var(--secondary-color)',
  },
  icon: {
    type: String,
    required: false,
    default: 'fas fa-box-open',
  },
})
</script>

<template>
  <div class="basic-box" :style="{ color, backgroundColor: bgColor, borderColor: color }">
    <svg-icon type="mdi" :path="icon" />
    <div class="body">
      <h2>{{ title }}</h2>
      <slot></slot>
    </div>
  </div>
</template>

<style lang="scss" scoped>
.basic-box {
  display: flex;
  flex-direction: row;
  align-items: center;
  padding: 10px;
  border: 2px solid;
  width: 300px;
  margin: 10px;

  svg {
    width: 30px;
    height: 30px;
    margin-right: 10px;
  }

  .body {
    display: flex;
    flex-direction: column;

    h2 {
      font-size: 20px;
      font-weight: bold;
    }
  }
}
</style>
