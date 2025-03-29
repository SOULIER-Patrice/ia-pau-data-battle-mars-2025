<script setup lang="ts">
import SvgIcon from '@jamescoyle/vue-icon'
import SpinnerLoader from '../Loaders/SpinnerLoader.vue'

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
  isLoading: {
    type: Boolean,
    default: false,
  },
  disabled: {
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
  <button
    v-if="isLoading"
    :disabled="isLoading"
    class="button"
    :style="{ color: color, backgroundColor: bgColor }"
  >
    <SpinnerLoader class="loader" :color="color" :size="1" />
  </button>
  <button
    v-else
    @click="onClick"
    :class="['button', { disabled: disabled }]"
    :style="{ color: color, backgroundColor: bgColor }"
  >
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

  &.disabled {
    cursor: not-allowed;
    opacity: 0.5;
  }
}
</style>
