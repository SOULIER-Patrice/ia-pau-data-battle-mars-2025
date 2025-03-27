<script setup lang="ts">
// Components
import BasicButton from '../Buttons/BasicButton.vue'

// Emits
defineEmits(['click'])

// Props
defineProps({
  title: {
    type: String,
    required: false,
  },
  buttonText: {
    type: String,
    required: false,
  },
  disabled: {
    type: Boolean,
    required: false,
    default: false,
  },
})
</script>

<template>
  <div class="card">
    <div class="title" v-if="title">
      <h3>{{ title }}</h3>
      <div class="line"></div>
    </div>
    <slot></slot>
    <div class="button-container">
      <BasicButton
        :text="buttonText"
        :class="[disabled ? 'button disabled' : 'button']"
        color="var(--secondary-text-color)"
        :bg-color="disabled ? '#999999' : 'var(--primary-color)'"
        @click="$emit('click')"
      />
    </div>
  </div>
</template>

<style scoped>
.card {
  display: flex;
  flex-direction: column;
  align-items: center;
  background-color: #e6e6e6;
  border-radius: 8px;
  box-shadow: 0 2px 4px 0 rgba(0, 0, 0, 0.1);
  padding: 16px;

  .title {
    width: 100%;
    display: flex;
    flex-direction: column;
    align-items: center;
    margin-bottom: 24px;

    h3 {
      font-size: 40px;
      color: var(--primary-text-color);
    }

    .line {
      width: 80%;
      height: 2px;
      background-color: var(--primary-color);
      margin-top: 8px;
    }
  }

  .button-container {
    margin-top: auto;
  }

  .button {
    margin-top: 24px;

    &.disabled {
      cursor: not-allowed;
    }
  }
}
</style>
