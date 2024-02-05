<script setup>
import { RouterLink, RouterView } from 'vue-router'
import Menu from 'primevue/menu'
import Menubar from 'primevue/menubar'
import Button from 'primevue/button'
import Avatar from 'primevue/avatar'
import { storeToRefs } from 'pinia'

import { ref } from 'vue'
import { useUserStore } from '@/store/user'
import router from '@/router/index.js'

const userStore = useUserStore()
const { getUserIsAuth } = storeToRefs(userStore)
const { logoutUser } = userStore

const menu = ref(null)
const menuItems = ref([
  {
    label: 'Logout',
    command: async () => {
      const { success } = await logoutUser()
      if (success) {
        await router.push({ name: 'login' })
      }
    }
  }
])

let toggle = (event) => {
  menu.value.toggle(event)
}
</script>

<template>
  <header>
    <Menubar>
      <template #start>
        <RouterLink to="/" class="text-3xl text-primary no-underline active:no-underline">
          Registration App
        </RouterLink>
      </template>
      <template v-if="getUserIsAuth" #end>
        <Button
          outlined
          type="button"
          aria-haspopup="true"
          aria-controls="overlay_menu"
          @click="toggle($event)"
        >
          <Avatar icon="pi pi-user" shape="circle" />
        </Button>
        <Menu id="overlay_menu" ref="menu" :model="menuItems" :popup="true" />
      </template>
    </Menubar>
  </header>

  <RouterView />
</template>

<style scoped></style>
