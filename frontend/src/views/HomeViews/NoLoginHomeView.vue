<script setup lang="ts">
// Stores
import { useAuthStore } from '@/stores/authStore'
import Logo from '@/assets/lawrag.png'

import router from '@/router'

const authStore = useAuthStore()
const user = authStore.user

// If the user is not logged in, redirect to the login page
if (!user) {
  router.push('/login')
}
</script>

<template>
  <div class="no-login-home-view">
    <div class="left">
      <p>Discover a new way</p>
      <p>to try, learn and</p>
      <p>succeed</p>
    </div>
    <div class="right">
      <div class="circle">
        <img :src="Logo" alt="Logo" width="280px" />
      </div>
    </div>
  </div>
</template>

<style lang="scss" scoped>
.no-login-home-view {
  display: flex;
  justify-content: center;
  align-items: center;
  flex: 1;
  font-size: 64px;
  font-weight: bold;

  .left {
    display: flex;
    flex-direction: column;
    justify-content: center;
    gap: 15px;
    height: 100%;
    width: 50%;

    p {
      margin: 0;
      margin-left: 100px;
    }
  }

  .right {
    display: flex;
    justify-content: center;
    align-items: center;
    width: 50%;
    height: 100%;

    .circle {
      width: 400px;
      height: 400px;
      display: flex;
      justify-content: center;
      align-items: center;
      margin-right: 50px;
      border-radius: 50%;
      background: radial-gradient(50% 50% at 50% 50%, #588157 0%, #3d5a3e 100%);
    }
  }
}
</style>
