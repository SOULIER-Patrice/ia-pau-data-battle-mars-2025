<script setup lang="ts">
import { ref } from 'vue'

const username = ref('')
const password = ref('')

const emit = defineEmits(['login'])

const handleSubmit = () => {
  emit('login', { username: username.value, password: password.value })
}
</script>

<template>
  <form @submit.prevent="handleSubmit">
    <div>
      <label for="username">Email</label>
      <input id="username" v-model="username" type="text" required />
    </div>
    <div>
      <label for="password">Firstname</label>
      <input id="password" v-model="password" type="password" required />
    </div>
    <button type="submit">Register</button>
  </form>
</template>

<style scoped lang="scss"></style>
