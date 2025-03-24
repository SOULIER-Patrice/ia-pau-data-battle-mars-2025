<script setup lang="ts">
import SvgIcon from '@jamescoyle/vue-icon'

defineProps({
  text: String,
  color: String,
  bgColor: String,
  icon: {
    type: String,
    required: false,
  },
  iconSize: {
    type: Number,
    default: 24,
  },
})

const emit = defineEmits(['click'])

const onClick = () => {
  emit('click')
}
</script>

<template>
  <button @click="onClick" class="button" :style="{ color: color, backgroundColor: bgColor }">
    <SvgIcon
      v-if="icon"
      type="mdi"
      :path="icon"
      :size="iconSize"
      :style="{ color: color }"
      class="icon"
    />
    {{ text }}
  </button>
</template>

<style lang="scss" scoped>
button {
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 5px 15px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  font-weight: bold;

  .icon {
    margin-left: -5px;
    margin-right: 5px;
  }
}
</style>
