<script setup>
import { RouterLink } from 'vue-router'
import Card from 'primevue/card'
import InputText from 'primevue/inputtext'
import Button from 'primevue/button'
import Divider from 'primevue/divider'
import Password from 'primevue/password'
import Message from 'primevue/message'

import { ref, nextTick } from 'vue'
import router from '@/router'
import { useUserStore } from '@/store/user'

const userStore = useUserStore()
const { registerUser } = userStore

const username = ref('')
const password = ref('')
const password2 = ref('')
const submitting = ref(false)
const errorMessage = ref()

const submitRegister = async () => {
  errorMessage.value = null
  if (username.value === '' || password.value === '' || password2.value === '') {
    await nextTick(() => {
      errorMessage.value = ['Please input all required fields.']
    })
    return
  }
  submitting.value = true
  const { success, errors } = await registerUser({
    username: username.value,
    password: password.value,
    password2: password2.value
  })
  if (success) {
    await router.push({
      name: 'login'
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
        <template #title>Register</template>
        <template #content>
          <transition-group name="p-message" tag="div">
            <Message v-for="(msg, index) in errorMessage" :key="index" severity="error">
              {{ msg }}
            </Message>
          </transition-group>
          <form @submit.prevent="submitting === false && submitRegister()">
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
            <div class="field">
              <label for="password2">Confirm Password</label>
              <Password
                v-model="password2"
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
                label="Register"
                class="flex align-items-center justify-content-center"
                icon="pi pi-user-plus"
              />
            </div>
            <Divider><b>OR</b></Divider>
            <div class="flex justify-content-between flex-wrap gap-5">
              <span class="flex align-items-center justify-content-center">Existing user?</span>
              <RouterLink to="/">
                <Button
                  label="Login"
                  severity="secondary"
                  class="flex align-items-center justify-content-center"
                  icon="pi pi-user"
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
