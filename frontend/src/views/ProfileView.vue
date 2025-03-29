<script setup lang="ts">
// Components
import UserForm from '@/components/Forms/UserForm.vue'

// Stores
import { useAuthStore } from '@/stores/authStore'
const authStore = useAuthStore()

const user = authStore.user

const updateUser = (args: any) => {
  if (!user) {
    return
  }
  authStore.updateUser(user.id, args.first_name, args.last_name, args.email)
}
</script>

<template>
  <div class="profile-view">
    <h1>Profile</h1>
    <UserForm :user="user" v-if="user" @update-user="updateUser" />
  </div>
</template>

<style lang="scss" scoped>
.profile-view {
  width: 100%;
  margin-top: 50px;
  display: flex;
  flex-direction: column;
  align-items: center;

  h1 {
    font-size: 64px;
    font-weight: bold;
    margin-bottom: 20px;
  }
}
</style>
