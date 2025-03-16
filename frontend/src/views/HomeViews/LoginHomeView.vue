<script setup lang="ts">
// Stores
import { useAuthStore } from '@/stores/authStore'

import router from '@/router'

const authStore = useAuthStore()
const user = authStore.user

// If the user is not logged in, redirect to the login page
if (!user) {
  router.push('/login')
}
</script>

<template>
  <div>
    <h1>Hello {{ user?.first_name }} !</h1>
  </div>
</template>

<style lang="scss" scoped></style>
