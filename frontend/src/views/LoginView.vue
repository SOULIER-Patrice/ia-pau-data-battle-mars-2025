<script setup lang="ts">
// Components
import LoginForm from '@/components/Forms/LoginForm.vue'
import RegiterForm from '@/components/Forms/RegiterForm.vue'

import router from '@/router'

// Stores
import { useAuthStore } from '@/stores/authStore'
import { ref } from 'vue'
import ActiveButton from '@/components/Buttons/ActiveButton.vue'
const authStore = useAuthStore()

const user = authStore.user
if (user) {
  router.push('/')
}

const isLogin = ref(true)
const isRegister = ref(false)

const toggleLogin = () => {
  isLogin.value = true
  isRegister.value = false
}

const toggleRegister = () => {
  isRegister.value = true
  isLogin.value = false
}

const login = async (args: any) => {
  await authStore.login(args.username, args.password)
}

const register = async (args: any) => {
  await authStore.register(args.email, args.password, args.first_name, args.last_name)
}
</script>

<template>
  <div class="login-view">
    <h1 v-if="isLogin">LOG IN</h1>
    <h1 v-else>SIGN UP</h1>
    <div class="buttons">
      <ActiveButton
        text="Login"
        color="black"
        bg-color="transparent"
        active-color="var(--secondary-text-color)"
        active-bg-color="var(--primary-color)"
        :style="{
          border: isLogin ? '' : 'none',
          borderRadius: '0 5px 5px 0',
        }"
        :isActive="isLogin"
        @click="toggleLogin"
      />
      <ActiveButton
        text="Signup"
        color="black"
        bg-color="transparent"
        active-color="var(--secondary-text-color)"
        active-bg-color="var(--primary-color)"
        :style="{
          border: isRegister ? '' : 'none',
          borderRadius: '5px 0 0 5px',
        }"
        :isActive="isRegister"
        @click="toggleRegister"
      />
    </div>

    <LoginForm v-if="isLogin" @login="login" />
    <RegiterForm v-else @register="register" />
  </div>
</template>

<style scoped lang="scss">
.login-view {
  h1 {
    font-size: 24px;
    font-weight: bold;
    color: var(--primary-text-color);
    margin-bottom: 10px;
  }

  margin-top: 50px;
  display: flex;
  flex-direction: column;
  align-items: center;

  .buttons {
    display: flex;
    border: 2px solid black;
    border-radius: 7px;
    overflow: hidden;

    button {
      width: 100px;
      font-weight: bold;
    }
  }
}
</style>
