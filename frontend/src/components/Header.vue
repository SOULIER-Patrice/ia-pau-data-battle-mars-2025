<!-- eslint-disable vue/multi-word-component-names -->
<script setup lang="ts"></script>

<template>
  <header>
    <router-link to="/" class="title">IA PAu Data Battle 2025</router-link>
    <nav>
      <router-link to="/">Événements</router-link>
      <router-link to="/about">À propos</router-link>
    </nav>
  </header>
</template>

<style lang="scss" scoped>
header {
  display: flex;
  justify-content: center;
  padding: 20px;
  background-color: #f0f0f0;
}

.title {
  font-size: 24px;
  font-weight: bold;
  text-decoration: none;
  color: var(--primary-text-color);
}
</style>
