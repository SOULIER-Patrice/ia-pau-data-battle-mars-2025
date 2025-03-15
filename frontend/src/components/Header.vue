<!-- eslint-disable vue/multi-word-component-names -->
<script setup lang="ts">
import { useAuthStore } from '@/stores/authStore'
import { computed } from 'vue'

const authStore = useAuthStore()
const user = computed(() => authStore.user)

const logout = () => {
  authStore.logout()
}
</script>

<template>
  <header>
    <router-link to="/" class="title">IA PAu Data Battle 2025</router-link>
    <nav>
      <router-link to="/about">About</router-link>
    </nav>
    <div>
      <div v-if="user">
        <span>{{ user.first_name }}</span>
        <button @click="logout">Logout</button>
      </div>
      <div v-else>
        <router-link to="/login">Login</router-link>
      </div>
    </div>
  </header>
</template>

<style lang="scss" scoped>
header {
  display: flex;
  justify-content: center;
  padding: 20px;
  background-color: #f0f0f0;
}

.title {
  font-size: 24px;
  font-weight: bold;
  text-decoration: none;
  color: var(--primary-text-color);
}
</style>
