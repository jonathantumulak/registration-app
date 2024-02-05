<script setup>
import { RouterView } from 'vue-router'
import Menubar from 'primevue/menubar'

import { getSession } from '@/services/api'
import { useUserStore } from '@/store/user'

const userStore = useUserStore()

const { setUserIsAuth } = userStore

getSession().then((response) => {
  setUserIsAuth(response.data['isAuthenticated'])
})
</script>

<template>
  <header>
    <Menubar>
      <template #start> Registration App </template>
      <template #end> </template>
    </Menubar>
  </header>

  <RouterView />
</template>

<style scoped></style>
