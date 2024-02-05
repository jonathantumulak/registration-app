<script setup>
import Card from 'primevue/card'
import Steps from 'primevue/steps'
import Divider from 'primevue/divider'

import PersonalSection from '@/components/PersonalSection.vue'
import JobSection from '@/components/JobSection.vue'
import InterestsSection from '@/components/InterestsSection.vue'

import { ref, reactive, computed, onMounted } from 'vue'
import { useUserStore } from '@/store/user.js'
import { storeToRefs } from 'pinia'

const userStore = useUserStore()
const { getProfileData } = storeToRefs(userStore)

const jobSectionDisabled = computed(() => {
  if (getProfileData.value) {
    const { first_name, last_name, birth_date, gender } = getProfileData.value
    return (first_name && last_name && birth_date && gender) !== 1
  }
  return false
})

const activeStep = ref(0)
const stepItems = reactive([
  {
    label: 'Personal Information'
  },
  {
    label: 'Job Preference',
    disabled: jobSectionDisabled.value
  },
  {
    label: 'Interests',
    disabled: true
  }
])

onMounted(() => {
  if (!jobSectionDisabled.value) {
    activeStep.value = 1
  }
})
</script>

<template>
  <main class="flex justify-content-center align-items-center flex-wrap w-screen">
    <div class="flex align-items-center justify-content-center font-bold border-round w-screen">
      <Card class="w-8 mt-5">
        <template #title>Welcome</template>
        <template #content>
          <Steps v-model:activeStep="activeStep" :model="stepItems" :readonly="false" />
          <Divider />
          <PersonalSection v-if="activeStep === 0" />
          <JobSection v-if="activeStep === 1" />
          <InterestsSection v-if="activeStep === 2" />
        </template>
      </Card>
    </div>
  </main>
</template>

<style scoped></style>
