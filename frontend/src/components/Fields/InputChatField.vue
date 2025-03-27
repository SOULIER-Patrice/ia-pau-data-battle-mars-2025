<script setup lang="ts">
import SvgIcon from '@jamescoyle/vue-icon'
import { mdiPencil, mdiSend } from '@mdi/js'
import { ref, onMounted } from 'vue'

defineProps({
  label: String,
  placeholder: {
    type: String,
    required: false,
    default: '',
  },
  isMessages: {
    type: Boolean,
    required: false,
    default: false,
  },
})

const emit = defineEmits(['submit'])

const emitSubmit = () => {
  emit('submit', model.value)
  model.value = ''
}

const model = defineModel<string>()

const isFocused = ref(false)

// Adjust textarea height dynamically
const adjustTextareaHeight = (event: Event) => {
  const textarea = event.target as HTMLTextAreaElement
  textarea.style.height = 'auto' // Reset height to calculate new height
  textarea.style.height = `${Math.min(textarea.scrollHeight, 150)}px` // Set height with a max limit
}

onMounted(() => {
  const textarea = document.querySelector('textarea')
  if (textarea) {
    textarea.style.height = 'auto'
  }
})
</script>

<template>
  <div :class="{ focused: isFocused || isMessages || model }">
    <SvgIcon type="mdi" :path="mdiPencil" />
    <textarea
      v-model="model"
      :placeholder="placeholder"
      @focus="isFocused = true"
      @blur="isFocused = false"
      @input="adjustTextareaHeight"
    ></textarea>
    <SvgIcon type="mdi" :path="mdiSend" @click="emitSubmit" class="submit" />
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
    transition: height 0.3s ease-in-out;
    max-height: 100px; // Limite maximale de hauteur
    overflow-y: auto; // Ajout d'un défilement si nécessaire

    &:focus {
      outline: none;
    }
  }

  &.focused {
    width: 450px;
    border: 2px solid black;
    border-radius: 7px;
  }

  .submit {
    cursor: pointer;
  }
}
</style>
