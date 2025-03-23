<script setup lang="ts"></script>

<template>
  <div class="no-login-home-view">
    <div class="left">
      <p>Discover a new way</p>
      <p>to try, learn and</p>
      <p>succeed</p>
    </div>
    <div class="right">
      <div class="circle"></div>
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
      margin-right: 50px;
      border-radius: 50%;
      background: radial-gradient(50% 50% at 50% 50%, #588157 0%, #3d5a3e 100%);
    }
  }
}
</style>
