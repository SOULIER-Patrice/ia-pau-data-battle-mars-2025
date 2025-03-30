<script setup lang="ts">
import Button from '../Buttons/BasicButton.vue'
import Chip from '../Chip.vue'

export type ItemListProps = {
  title?: string
  description?: string
  href?: string
  buttons?: any[]
  chips?: any[]
}

const props = defineProps<ItemListProps>()
</script>

<template>
  <div :class="['container']">
    <router-link v-if="props.href" :to="props.href" custom v-slot="{ navigate }">
      <div @click="navigate" role="link">
        <div class="content">
          <div class="left">
            <div class="leftText">
              <div class="title">{{ props.title }}</div>
              <div v-if="props.description" class="description">{{ props.description }}</div>
            </div>
          </div>
          <div v-if="props.chips" class="chipsContainer">
            <Chip
              v-for="(chip, index) in props.chips"
              :key="index"
              :title="chip.title"
              :color="chip.color"
              :bgColor="chip.bgColor"
              class="chip"
            />
          </div>
          <div v-if="props.buttons" class="chipsContainer">
            <Button
              v-for="(button, index) in props.buttons"
              :key="index"
              :title="button.title"
              @click.prevent.stop="button.onPress"
              :color="button.color"
              :icon="button.icon"
              :width="button.width"
              :height="button.height"
              :padding="button.padding"
              class="chip"
            />
          </div>
        </div>
      </div>
    </router-link>
  </div>
</template>

<style scoped lang="scss">
.container {
  padding: 0 5px;
  border-bottom-width: 1px;
  border-color: lightgrey;
  width: 100%;
}
.content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;

  &:hover {
    background-color: #f0f0f0;
    cursor: pointer;
  }
}
.left {
  display: flex;
  align-items: center;
  flex: 1;
}
.leftText {
  flex: 1;
}
.checkbox {
  margin-right: 10px;
}
.chipsContainer {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
}
.chip {
  margin: 5px 0;
}
.title {
  font-size: 16px;
  font-weight: bold;
  margin-right: 15px;
}
.description {
  font-size: 14px;
  color: grey;
  margin-right: 15px;
}
</style>
