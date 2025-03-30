<script setup lang="ts">
// Components
import List from '@/components/List/List.vue'
import SpinnerLoader from '@/components/Loaders/SpinnerLoader.vue'

// Stores
import { useAuthStore } from '@/stores/authStore'
import type { Item } from '@/types/Item'
import type { User } from '@/types/User'
import { ref, watch } from 'vue'
const authStore = useAuthStore()

const apiUrl = import.meta.env.VITE_BASE_API_URL

const users = ref<User[]>([])
const isLoading = ref(false)

// Fonction pour transformer les données User en Items
const transformUserToItems = (users: User[]): Item[] => {
  return users.map((user) => ({
    title: `${user.first_name} ${user.last_name}`, // Titre avec prénom et nom
    description: user.email, // Description avec l'email
    href: `/users/${user.id}`, // Lien vers la page utilisateur
  }))
}

// Fetch user data
const fetchUserData = async () => {
  try {
    const response = await fetch(`${apiUrl}/users`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${authStore.token?.access_token}`,
      },
    })

    if (!response.ok) {
      throw new Error('Failed to fetch user data')
    }

    const data = await response.json()
    users.value = data
  } catch (error) {
    console.error('Error fetching user data:', error)
  }
}
watch(
  () => authStore.token,
  (newToken) => {
    if (newToken) {
      fetchUserData()
    }
  },
  { immediate: true },
)
</script>

<template>
  <div class="admin-user-view">
    <h1>Admin User Management</h1>
    <p>Manage users from this view.</p>
    <SpinnerLoader v-if="isLoading" />
    <div v-else>
      <List :items="transformUserToItems(users)" :title="'Users List'" class="user-list" />
    </div>
    <router-link to="/admin">Back to Admin Home</router-link>
  </div>
</template>

<style scoped lang="scss">
.admin-user-view {
  display: flex;
  width: 100%;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 20px;

  h1 {
    font-size: 64px;
    color: var(--primary-text-color);
  }

  p {
    font-size: 20px;
    color: var(--primary-text-color);
  }

  .user-list {
    width: 600px;
    margin: 0 auto;
  }
}
</style>
