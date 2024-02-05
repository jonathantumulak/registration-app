<script setup>
import { RouterLink, RouterView } from 'vue-router'
import Menubar from 'primevue/menubar'
</script>

<template>
  <header>
    <Menubar>
      <template #start>
        <RouterLink to="/"> Registration App </RouterLink>
      </template>
      <template #end></template>
    </Menubar>
  </header>

  <RouterView />
</template>

<style scoped></style>
