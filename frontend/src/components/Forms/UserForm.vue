<script setup lang="ts">
import { ref } from 'vue'

// Components
import InputField from '../Fields/InputField.vue'
import BasicButton from '../Buttons/BasicButton.vue'
import ErrorBox from '../Boxes/ErrorBox.vue'

const props = defineProps({
  user: {
    type: Object,
    required: true,
  },
})

const email = ref(props.user.email)
const firstName = ref(props.user.first_name)
const lastName = ref(props.user.last_name)
const errors = ref<string[]>([])

const emit = defineEmits(['updateUser'])

const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/

const handleSubmit = () => {
  errors.value = []
  if (!emailRegex.test(email.value)) {
    errors.value.push('Invalid email!')
  }

  if (errors.value.length === 0) {
    emit('updateUser', {
      email: email.value,
      first_name: firstName.value,
      last_name: lastName.value,
    })
  }
}
</script>

<template>
  <ErrorBox v-for="error in errors" :key="error" v-if="errors.length > 0">
    {{ error }}
  </ErrorBox>
  <form @submit.prevent="handleSubmit">
    <InputField v-model="firstName" label="First Name" placeholder="John" />
    <InputField v-model="lastName" label="Last Name" placeholder="Doe" />
    <InputField v-model="email" label="Email" placeholder="john.doe@example.com" />
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
  width: 300px;
  margin-top: 30px;
  background-color: #e6e6e6;
  border-radius: 12px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
  padding: 30px 10px;

  button {
    width: 100px;
    align-self: flex-end;
    font-weight: bold;
  }
}
</style>
