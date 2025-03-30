<script setup lang="ts">
import { ref, computed } from 'vue'

import type { QA } from '@/types/QA'

// Components
import TextAreaField from '../Fields/TextAreaField.vue'
import BasicButton from '../Buttons/BasicButton.vue'
import ErrorBox from '../Boxes/ErrorBox.vue'

const props = defineProps({
  qa: {
    type: Object as () => QA,
    required: true,
  },
})

const question = ref(props.qa.question)
const answer = ref(props.qa.answer)
const categories = ref(props.qa.category)
const is_verified = ref(props.qa.is_verified)
const options = ref(props.qa.options || [])
const justification = ref(props.qa.justification)

const categories_list = [
  'Filing requirements and formalities',
  'Priority claims and right of priority',
  'Divisional applications',
  'Fees, payment methods, and time limits',
  'Languages and translations',
  'Procedural remedies and legal effect',
  'Pct procedure and entry into the european phase',
  'Examination, amendments, and grant',
  'Opposition and appeals',
  'Substantive patent law: novelty and inventive step',
  'Entitlement and transfers',
  'Biotech and sequence listings',
  'Unity of invention',
]

const errors = ref<string[]>([])

const emit = defineEmits(['updateQuestion'])

const isMCQ = computed(() => props.qa.type === 'MCQ')

const handleSubmit = () => {
  errors.value = []

  if (errors.value.length === 0) {
    emit('updateQuestion', {
      id: props.qa.id,
      type: props.qa.type,
      category: categories.value,
      question: question.value,
      answer: answer.value,
      is_verified: is_verified.value,
      options: options.value,
      justification: justification.value,
    } as QA)
  }
}

const addOption = () => {
  options.value.push('')
}

const removeOption = (index: number) => {
  options.value.splice(index, 1)
}
</script>

<template>
  <ErrorBox v-for="error in errors" :key="error" v-if="errors.length > 0">
    {{ error }}
  </ErrorBox>
  <form @submit.prevent="handleSubmit">
    <TextAreaField v-model="question" label="Question" placeholder="What is Vue.js?" />
    <TextAreaField
      v-model="answer"
      label="Answer"
      placeholder="A JavaScript framework for building UIs"
    />
    <label for="categories">Category</label>
    <select id="categories" v-model="categories">
      <option v-for="category in categories_list" :key="category" :value="category">
        {{ category }}
      </option>
    </select>
    <label for="is_verified">Is Verified?</label>
    <select id="is_verified" v-model="is_verified">
      <option :value="true">True</option>
      <option :value="false">False</option>
    </select>

    <div v-if="isMCQ" class="options">
      <label>Options</label>
      <div v-for="(option, index) in options" :key="index" class="option-field">
        <TextAreaField
          v-model="options[index]"
          :label="'Option ' + (index + 1)"
          placeholder="Enter option"
        />
        <button type="button" @click="removeOption(index)">Remove</button>
      </div>
      <button type="button" @click="addOption">Add Option</button>
    </div>

    <TextAreaField
      v-if="isMCQ"
      v-model="justification"
      label="Justification"
      placeholder="Explain your answer here..."
    />

    <BasicButton
      text="Modify"
      color="var(--secondary-text-color)"
      bg-color="var(--primary-color)"
      type="submit"
    />
  </form>
</template>

<style scoped lang="scss">
form {
  display: flex;
  flex-direction: column;
  gap: 20px;
  width: 700px;
  margin-top: 30px;
  background-color: #ffffff;
  border-radius: 12px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
  padding: 30px 10px;

  button {
    width: 100px;
    align-self: flex-end;
    font-weight: bold;
  }

  select {
    padding: 10px;
    border-radius: 5px;
    border: 1px solid #ccc;
  }

  .options {
    display: flex;
    flex-direction: column;
    gap: 10px;
    margin-top: 20px;

    label {
      font-weight: bold;
      margin-bottom: 5px;
    }
  }

  .option-field {
    display: flex;
    align-items: center;
    gap: 10px;

    button {
      background-color: #ff4d4d;
      color: white;
      border: none;
      border-radius: 5px;
      padding: 5px 10px;
      cursor: pointer;
    }
  }
}
</style>
