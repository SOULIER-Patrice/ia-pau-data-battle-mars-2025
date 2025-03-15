<script setup lang="ts">
// Components
import LoginForm from '@/components/Forms/LoginForm.vue'
import RegiterForm from '@/components/Forms/RegiterForm.vue'
import router from '@/router'

// Stores
import { useAuthStore } from '@/stores/authStore'
import { ref } from 'vue'
const authStore = useAuthStore()

const user = authStore.user
if (user) {
  router.push('/')
}

const toggleLogin = ref(true)

const login = async (args: any) => {
  await authStore.login(args.username, args.password)
}
</script>

<template>
  <div class="about">
    <h1>Login</h1>
    <button @click="toggleLogin = !toggleLogin">Toggle</button>
    <LoginForm v-if="toggleLogin" @login="login" />
    <RegiterForm v-else />
  </div>
</template>

<style scoped lang="scss"></style>
