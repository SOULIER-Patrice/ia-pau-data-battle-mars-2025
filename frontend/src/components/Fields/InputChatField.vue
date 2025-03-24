<script setup lang="ts">
import SvgIcon from '@jamescoyle/vue-icon'
import { mdiPencil, mdiSend } from '@mdi/js'
import { ref } from 'vue'

defineProps({
  label: String,
  placeholder: {
    type: String,
    required: false,
    default: '',
  },
})

const model = defineModel<string>()

const isFocused = ref(false)
</script>

<template>
  <div :class="{ focused: isFocused }">
    <SvgIcon type="mdi" :path="mdiPencil" />
    <textarea
      v-model="model"
      :placeholder="placeholder"
      @focus="isFocused = true"
      @blur="isFocused = false"
    ></textarea>
    <SvgIcon type="mdi" :path="mdiSend" />
  </div>
</template>

<style lang="scss" scoped>
div {
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: space-between;
  background-color: white;
  border-radius: 10px;
  padding: 5px;
  width: 250px;
  transition: width 0.3s ease-in-out;

  textarea {
    padding: 5px;
    flex: 1;
    border: none;
    background-color: transparent;
    resize: none;
    height: 20px;
    transition: height 0.3s ease-in-out;

    &:focus {
      outline: none;
      height: 50px;
    }
  }

  &.focused {
    width: 450px;
    border: 2px solid black;
    border-radius: 7px;
  }
}
</style>
