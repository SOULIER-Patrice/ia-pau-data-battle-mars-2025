<script setup lang="ts">
import { ref } from 'vue'

// Components
import InputField from '../Fields/InputField.vue'
import BasicButton from '../Buttons/BasicButton.vue'
import ErrorBox from '../Boxes/ErrorBox.vue'

const email = ref('')
const password = ref('')
const confirmPassword = ref('')
const firstName = ref('')
const lastName = ref('')
const errors = ref<string[]>([])

const emit = defineEmits(['register'])

const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/

const handleSubmit = () => {
  errors.value = []
  if (!emailRegex.test(email.value)) {
    errors.value.push('Invalid email!')
  }

  if (password.value !== confirmPassword.value) {
    errors.value.push('Passwords do not match!')
  }

  if (errors.value.length === 0) {
    emit('register', {
      email: email.value,
      password: password.value,
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
    <InputField v-model="password" label="Password" type="password" />
    <InputField v-model="confirmPassword" label="Confirm Password" type="password" />
    <BasicButton
      text="Signup"
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

  button {
    width: 100px;
    align-self: flex-end;
    font-weight: bold;
  }
}
</style>
