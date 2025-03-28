<!-- eslint-disable vue/multi-word-component-names -->
<script setup lang="ts">
import { useAuthStore } from '@/stores/authStore'
import { computed, ref } from 'vue'

// Components
import LinkActiveButton from './Buttons/LinkActiveButton.vue'
import BasicButton from './Buttons/BasicButton.vue'
import SvgIcon from '@jamescoyle/vue-icon'
import { mdiAccountCircleOutline } from '@mdi/js'
import Logo from '@/assets/lawrag.png'

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

const isExpanded = ref(false)
const toggleExpanded = () => {
  isExpanded.value = !isExpanded.value
}
</script>

<template>
  <header>
    <router-link to="/" class="title">
      <img :src="Logo" alt="Logo" width="100px" />
    </router-link>
    <nav>
      <LinkActiveButton text="Home" :isActive="activeTab === '/'" to="/" />
      <LinkActiveButton text="Practice" :isActive="activeTab === '/practice'" to="/practice" />
      <!-- <LinkActiveButton text="About" :isActive="activeTab === '/about'" to="/about" /> -->
    </nav>
    <div class="auth">
      <div v-if="user">
        <SvgIcon
          type="mdi"
          :path="mdiAccountCircleOutline"
          :size="32"
          color="black"
          @click="toggleExpanded"
          class="profile-icon"
        />
        <div class="extended-panel" v-if="isExpanded">
          <div class="title">
            <h2>Profile</h2>
          </div>
          <div class="body">
            <nav>
              <router-link to="/profile" @click="toggleExpanded">Settings</router-link>
            </nav>
            <BasicButton text="Logout" @click="logout" />
          </div>
        </div>
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
  z-index: 1002;
  align-items: center;

  nav {
    display: flex;

    margin-right: 20px;

    button {
      margin-right: 10px;
    }
  }

  .auth {
    margin-left: auto;
    margin-right: 75px;
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

    .extended-panel {
      position: absolute;
      width: 120px;
      top: 60px;
      right: 50px;
      background-color: #f4f3f3;
      border-radius: 5px;
      display: flex;
      flex-direction: column;
      align-items: center;
      z-index: 1005;
      overflow: hidden;

      .title {
        display: flex;
        flex-direction: row;
        align-items: center;
        justify-content: center;
        width: 100%;
        background-color: var(--primary-color);
        color: white;
        margin-right: 0;
        padding: 5px 0;

        img {
          width: 30px;
          height: 30px;
          margin-right: 5px;
        }

        h2 {
          font-family: 'Konkhmer Sleokchher';
          font-size: 18px;
        }
      }

      .body {
        display: flex;
        flex-direction: column;
        align-items: center;
        width: 100%;
        padding: 10px 0;

        nav {
          width: 100%;
          display: flex;
          flex-direction: column;
          align-items: center;
          gap: 10px;
          padding: 5px 0;
          margin-bottom: 5px;

          a {
            text-decoration: none;
            color: var(--primary-text-color);
          }
        }
      }
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

.profile-icon {
  cursor: pointer;
}
</style>
