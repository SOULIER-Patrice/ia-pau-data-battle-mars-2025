<script setup lang="ts">
// Components
import BasicCard from '@/components/Cards/BasicCard.vue'
</script>

<template>
  <div class="select-mode-view">
    <h1>Which way to practice ?</h1>
    <div class="cards">
      <BasicCard
        title="Multiple-responses"
        buttonText="Choose this option"
        link="/practices/choose"
      >
        <div class="select-mode-view__content">
          <p>This category consists to choose one answer between different responses.</p>
        </div>
      </BasicCard>
      <BasicCard title="Free response" buttonText="Choose this option" link="/practices/random">
        <div class="select-mode-view__content">
          <p>This category consists to write your own answer.</p>
        </div>
      </BasicCard>
    </div>
  </div>
</template>

<style lang="scss" scoped>
.select-mode-view {
  display: flex;
  flex: 1;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  gap: 50px;

  h1 {
    font-size: 64px;
    color: var(--primary-text-color);
  }

  .cards {
    display: flex;
    gap: 100px;

    .card {
      width: 400px;
      height: 300px;
    }

    .select-mode-view__content {
      p {
        font-size: 1rem;
        font-weight: normal;
        color: var(--primary-text-color);
      }
    }
  }
}
</style>
.
