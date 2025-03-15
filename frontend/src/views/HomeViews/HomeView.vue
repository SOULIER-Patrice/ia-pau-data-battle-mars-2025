<script setup lang="ts">
// Views
import { computed } from 'vue'
import LoginHomeView from './LoginHomeView.vue'
import NoLoginHomeView from './NoLoginHomeView.vue'

// Stores
import { useAuthStore } from '@/stores/authStore'

const authStore = useAuthStore()
const user = computed(() => authStore.user)
</script>

<template>
  <div>
    <NoLoginHomeView v-if="!user" />
    <LoginHomeView v-else />
  </div>
</template>

<style lang="scss" scoped></style>
