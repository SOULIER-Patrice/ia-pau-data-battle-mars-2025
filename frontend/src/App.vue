<script setup lang="ts">
import { RouterView, useRoute } from 'vue-router'
import Header from './components/Header.vue'
import Footer from './components/Footer.vue'
import { computed, ref, watch } from 'vue'

const route = useRoute()
const isLoginRoute = computed(() => route.path === '/login')
const componentKey = ref(Date.now())

// Watch for route changes and reload the component
watch(
  () => route,
  () => {
    componentKey.value = Date.now()
  },
  { deep: true }, // Surveille les changements profonds
)
</script>

<template>
  <div class="container" v-if="!isLoginRoute">
    <Header class="header" />
    <div class="page">
      <main>
        <RouterView :key="componentKey" />
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

.header {
  position: fixed;
  width: 100%;
}

.page {
  margin-top: 79px;
  display: flex;
  flex: 1;

  main {
    display: flex;
    flex: 1;
  }
}
</style>
