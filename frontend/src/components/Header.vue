<!-- eslint-disable vue/multi-word-component-names -->
<script setup lang="ts">
import { useAuthStore } from '@/stores/authStore'

const { login, logout, keycloak, user } = useAuthStore()
</script>

<template>
  <header>
    <router-link to="/" class="title">Corpauration</router-link>
    <nav>
      <router-link to="/">Événements</router-link>
      <router-link to="/about">À propos</router-link>
    </nav>

    <button v-if="!keycloak.authenticated" @click="() => login({})">Se connecter</button>
    <div v-else>
      <span>{{ `${user?.firstName} ${user?.lastName}` }}</span>
      <button @click="() => logout({})">Se déconnecter</button>
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
