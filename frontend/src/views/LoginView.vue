<script setup>
import { RouterLink } from 'vue-router'
import Card from 'primevue/card'
import InputText from 'primevue/inputtext'
import Button from 'primevue/button'
import Divider from 'primevue/divider'
import Password from 'primevue/password'
import Message from 'primevue/message'

import { nextTick, ref } from 'vue'
import { storeToRefs } from 'pinia'
import { useUserStore } from '@/store/user'
import router from '@/router/index.js'

const userStore = useUserStore()
const { getUserNewRegistered } = storeToRefs(userStore)
const { loginUser } = userStore

const username = ref('')
const password = ref('')
const submitting = ref(false)
const errorMessage = ref()

const submitLogin = async () => {
  errorMessage.value = null
  if (username.value === '' || password.value === '') {
    nextTick(() => {
      errorMessage.value = ['Please input username and/or password.']
    })
    return
  }
  submitting.value = true
  const { success, errors } = await loginUser({
    username: username.value,
    password: password.value
  })
  if (success) {
    await router.push({
      name: 'home'
    })
  } else {
    if (errors) {
      errorMessage.value = errors
      submitting.value = false
    }
  }
}
</script>

<template>
  <main class="flex justify-content-center align-items-center flex-wrap">
    <div class="flex align-items-center justify-content-center font-bold border-round">
      <Card class="mt-5">
        <template #title>Login</template>
        <template #content>
          <Message v-if="getUserNewRegistered">Registered successfully. Login to proceed.</Message>
          <transition-group name="p-message" tag="div">
            <Message v-for="(msg, index) in errorMessage" :key="index" severity="error">{{
              msg
            }}</Message>
          </transition-group>
          <form @submit.prevent="submitting === false && submitLogin()">
            <div class="field">
              <label for="username">Username</label>
              <InputText
                v-model="username"
                type="text"
                class="text-base text-color surface-overlay p-2 border-1 border-solid surface-border border-round appearance-none outline-none focus:border-primary w-full"
              />
            </div>
            <div class="field">
              <label for="password">Password</label>
              <Password
                v-model="password"
                :feedback="false"
                class="w-full"
                :pt="{
                  input: {
                    root: {
                      class: ['w-full']
                    }
                  }
                }"
              />
            </div>
            <div class="flex justify-content-end flex-wrap">
              <Button
                :loading="submitting"
                type="submit"
                label="Login"
                class="flex align-items-center justify-content-center"
                icon="pi pi-user"
              />
            </div>
            <Divider><b>OR</b></Divider>
            <div class="flex justify-content-between flex-wrap gap-5">
              <span class="flex align-items-center justify-content-center">New user?</span>
              <RouterLink to="/register">
                <Button
                  label="Register"
                  severity="secondary"
                  class="flex align-items-center justify-content-center"
                  icon="pi pi-user-plus"
                />
              </RouterLink>
            </div>
          </form>
        </template>
      </Card>
    </div>
  </main>
</template>

<style scoped></style>
