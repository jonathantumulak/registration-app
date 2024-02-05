<script setup>
import { RouterView } from 'vue-router'
import Menubar from 'primevue/menubar';

import { ref } from 'vue'


</script>

<template>
  <Menubar>
    <template #start>
      Registration App
    </template>
    <template #end>
    </template>
  </Menubar>

  <RouterView />
</template>

<style scoped></style>
