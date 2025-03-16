<script setup lang="ts">
// Components
import LoginForm from '@/components/Forms/LoginForm.vue'
import RegiterForm from '@/components/Forms/RegiterForm.vue'
import SvgIcon from '@jamescoyle/vue-icon'
import { mdiArrowLeft } from '@mdi/js'

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
    <SvgIcon
      type="mdi"
      :path="mdiArrowLeft"
      :size="24"
      class="back-arrow"
      @click="router.push('/')"
    />
    <div class="left">
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
    <div class="right">
      <h1>IA PAU DATA BATTLE 2025</h1>
    </div>
  </div>
</template>

<style scoped lang="scss">
.login-view {
  display: flex;
  justify-content: center;
  height: 100vh;
}

.back-arrow {
  position: absolute;
  top: 20px;
  left: 20px;
  cursor: pointer;
}

.left {
  h1 {
    font-size: 24px;
    font-weight: bold;
    color: var(--primary-text-color);
    margin-bottom: 10px;
  }

  margin-top: 250px;
  display: flex;
  flex-direction: column;
  align-items: center;
  width: 50%;

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

.right {
  width: 50%;
  height: 100%;
  background: linear-gradient(153.69deg, #588157 0%, #3d5a3e 71.11%);
  display: flex;
  justify-content: center;
  align-items: center;

  h1 {
    font-size: 40px;
    font-weight: bold;
    color: white;
  }
}
</style>
