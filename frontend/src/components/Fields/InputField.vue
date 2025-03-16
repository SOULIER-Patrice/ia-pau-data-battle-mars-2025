<script setup lang="ts">
defineProps({
  label: String,
  placeholder: {
    type: String,
    required: false,
    default: '',
  },
  type: {
    type: String,
    required: false,
    default: 'text',
  },
})

const model = defineModel()
</script>

<template>
  <div>
    <label>{{ label }}</label>
    <input v-model="model" :placeholder="placeholder" :type="type" />
  </div>
</template>

<style lang="scss" scoped>
div {
  display: flex;
  flex-direction: column;
  width: 100%;

  label {
    font-weight: bold;
    margin-bottom: 2px;
  }

  input {
    padding: 5px;
    border: 2px solid black;
    border-radius: 7px;
  }
}
</style>
