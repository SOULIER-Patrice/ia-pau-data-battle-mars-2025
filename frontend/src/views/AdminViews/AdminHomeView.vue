<script setup lang="ts"></script>

<template>
  <div class="admin-home-view">
    <h1>Admin Home</h1>
    <p>Welcome to the admin home view!</p>
    <router-link to="/admin/users">Manage Users</router-link>
    <router-link to="/admin/qa">Manage Questions/Answers</router-link>
  </div>
</template>

<style scoped lang="scss">
.admin-home-view {
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
    font-size: 1rem;
    font-weight: normal;
    color: var(--primary-text-color);
  }

  a {
    font-size: 1.5rem;
    color: var(--primary-text-color);
    text-decoration: none;

    &:hover {
      text-decoration: underline;
    }
  }
}
</style>
