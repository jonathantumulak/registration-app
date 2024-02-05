<script setup>
import Message from 'primevue/message'
import Listbox from 'primevue/listbox'

import { onMounted, ref } from 'vue'
// import { useUserStore } from '@/store/user.js'
import { useInterestsStore } from '@/store/interest.js'
import Button from 'primevue/button'
// import { storeToRefs } from "pinia";

// const userStore = useUserStore()
// const {  } = storeToRefs(userStore)
// const {  } = userStore

const interestsStore = useInterestsStore()
const { getInterests } = interestsStore

const interestOptions = ref([])
const selectedInterests = ref([])
const submitting = ref(false)
const errorMessage = ref()

onMounted(async () => {
  const { data } = await getInterests()
  interestOptions.value = data
})

const submitInterests = async () => {}
</script>

<template>
  <div class="text-xl font-semibold text-center">Select your interests</div>
  <transition-group name="p-message" tag="div">
    <Message v-for="(msg, index) in errorMessage" :key="index" severity="error">
      {{ msg }}
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
