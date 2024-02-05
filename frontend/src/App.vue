<script setup>
import { RouterView } from 'vue-router'
import Menubar from 'primevue/menubar'


</script>

<template>
  <header>
    <Menubar>
      <template #start>
        Registration App
      </template>
      <template #end>
      </template>
    </Menubar>
  </header>

  <RouterView />
</template>

<style scoped>
</style>
