<script setup lang="ts">
import { RouterView, useRoute } from 'vue-router'
import Header from './components/Header.vue'
import Footer from './components/Footer.vue'
import { computed } from 'vue'

const route = useRoute()
const isLoginRoute = computed(() => route.path === '/login')
</script>

<template>
  <div class="container" v-if="!isLoginRoute">
    <Header />
    <div class="page">
      <main>
        <RouterView />
      </main>
    </div>
    <Footer />
  </div>
  <RouterView v-else />
</template>

<style lang="scss" scoped>
.container {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

.page {
  flex: 1;
}
</style>
