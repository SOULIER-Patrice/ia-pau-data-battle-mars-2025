<script setup lang="ts">
import { ref } from 'vue'

// Stores
import { useAuthStore } from '@/stores/authStore'
const authStore = useAuthStore()

// Components
import InputField from '../Fields/InputField.vue'
import BasicButton from '../Buttons/BasicButton.vue'

const username = ref('')
const password = ref('')

const emit = defineEmits(['login'])

const handleSubmit = () => {
  emit('login', { username: username.value, password: password.value })
}
</script>

<template>
  <form @submit.prevent="handleSubmit">
    <InputField v-model="username" label="Email" placeholder="john.doe@example.com" />
    <div class="password">
      <InputField v-model="password" label="Password" type="password" />
      <a href="#">Forgot password ?</a>
    </div>
    <BasicButton
      text="Login"
      color="var(--secondary-text-color)"
      bg-color="var(--primary-color)"
      type="submit"
      :is-loading="authStore.isLoading"
    />
  </form>
</template>

<style scoped lang="scss">
form {
  display: flex;
  flex-direction: column;
  gap: 30px;
  width: 300px;
  margin-top: 30px;

  button {
    width: 100px;
    align-self: flex-end;
    font-weight: bold;
  }

  .password {
    a {
      font-size: 12px;
      color: var(--primary-text-color);
    }
  }
}
</style>
