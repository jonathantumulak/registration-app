<script setup>
import Message from 'primevue/message'
import Listbox from 'primevue/listbox'
import Button from 'primevue/button'

import { nextTick, onMounted, ref, watch } from 'vue'
import { useUserStore } from '@/store/user.js'
import { useInterestsStore } from '@/store/interest.js'
import { storeToRefs } from 'pinia'
import router from '@/router/index.js'

const userStore = useUserStore()
const { getUserInterestsData } = storeToRefs(userStore)
const { getUserInterests, updateUserInterests } = userStore

const interestsStore = useInterestsStore()
const { getAllInterests } = interestsStore

const interestOptions = ref([])
const selectedInterests = ref([])
const submitting = ref(false)
const message = ref()
const errorMessage = ref()

onMounted(async () => {
  const { data } = await getAllInterests()
  interestOptions.value = data

  getUserInterests()
})

watch(getUserInterestsData, (userInterests) => {
  if (userInterests && userInterests.length >= 0) {
    selectedInterests.value = userInterests.map((el) => el.id)
  }
})

const submitInterests = async () => {
  errorMessage.value = null
  if (selectedInterests.value === []) {
    await nextTick(() => {
      errorMessage.value = ['Please select an interest']
    })
    return
  }
  submitting.value = true
  const { success, errors } = await updateUserInterests({
    interests: selectedInterests.value
  })
  if (success) {
    submitting.value = false
    message.value = 'Information updated'
    await router.push({ name: 'home' })
  } else {
    if (errors) {
      errorMessage.value = errors
      submitting.value = false
    }
  }
}
</script>

<template>
  <div class="text-xl font-semibold text-center">Select your interests</div>
  <transition-group name="p-message" tag="div">
    <Message v-for="(msg, index) in errorMessage" :key="index" severity="error">
      {{ msg }}
    </Message>
    <Message v-if="message">
      {{ message }}
    </Message>
  </transition-group>
  <form @submit.prevent="submitting === false && submitInterests()">
    <div class="flex justify-content-center align-items-center flex-wrap w-full">
      <Listbox
        v-model="selectedInterests"
        :options="interestOptions"
        option-label="name"
        option-value="id"
        class="mt-5 w-full md:w-14rem"
        multiple
      />
    </div>
    <div class="flex justify-content-end flex-wrap">
      <Button
        :loading="submitting"
        type="submit"
        label="Update Information"
        class="flex align-items-center justify-content-center"
      />
    </div>
  </form>
</template>

<style scoped></style>
