<!-- eslint-disable vue/multi-word-component-names -->
<script setup lang="ts">
import { useAuthStore } from '@/stores/authStore'
import { computed } from 'vue'
import LinkActiveButton from './Buttons/LinkActiveButton.vue'
import BasicButton from './Buttons/BasicButton.vue'

import { useRouter } from 'vue-router'
const router = useRouter()

import { useRoute } from 'vue-router'
const route = useRoute()

const authStore = useAuthStore()
const user = computed(() => authStore.user)

const logout = () => {
  authStore.logout()
}

const activeTab = computed(() => {
  return route.path
})
</script>

<template>
  <header>
    <router-link to="/" class="title">IA Pau Data Battle 2025</router-link>
    <nav>
      <LinkActiveButton text="Home" :isActive="activeTab === '/'" to="/" />
      <LinkActiveButton text="About" :isActive="activeTab === '/about'" to="/about" />
    </nav>
    <div class="auth">
      <div v-if="user">
        <BasicButton text="Logout" @click="logout" />
      </div>
      <div v-else>
        <BasicButton text="Login" @click="router.push('/login')" />
      </div>
    </div>
  </header>
</template>

<style lang="scss" scoped>
header {
  display: flex;
  padding: 20px;
  background-color: #f4f3f3;
  align-items: center;

  nav {
    margin-right: 20px;

    button {
      margin-right: 10px;
    }
  }

  .auth {
    margin-left: auto;
    display: flex;
    align-items: center;

    button {
      padding: 5px 10px;
      border: none;
      border-radius: 5px;
      cursor: pointer;
      background-color: var(--primary-color);
      color: white;
    }
  }
}

.title {
  font-size: 24px;
  font-weight: bold;
  text-decoration: none;
  color: var(--primary-text-color);
  margin-right: 30px;
}
</style>
