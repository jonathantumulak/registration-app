<script setup>
import Card from 'primevue/card'
import DataTable from 'primevue/datatable'
import Column from 'primevue/column'
import Chip from 'primevue/chip'

import { onMounted, ref, watch } from 'vue'
import { genderMap, experienceLevelMap } from '@/services/constants.js'
import { useUserStore } from '@/store/user.js'
import { storeToRefs } from 'pinia'
import Divider from 'primevue/divider'
const userStore = useUserStore()
const { getProfileData, getJobPreferenceData, getUserInterestsData } = storeToRefs(userStore)
const { getProfile, getJobPreference, getUserInterests } = userStore

const profileData = ref([])
const jobPrefData = ref([])
const interestsData = ref([])

const setProfileData = (value) => {
  profileData.value = [
    { label: 'First name', value: value['first_name'] },
    { label: 'Last name', value: value['last_name'] },
    { label: 'Birth date', value: value['birth_date'] },
    { label: 'Gender', value: genderMap[value['gender']] }
  ]
}

const setJobPrefData = (value) => {
  jobPrefData.value = [
    { label: 'Experience level', value: experienceLevelMap[value['experience_level']] },
    { label: 'Expected salary', value: value['expected_salary'] }
  ]
}

const setInterestsData = (value) => {
  interestsData.value = value.map((el) => el.name)
}

onMounted(() => {
  if (getProfileData.value === null) {
    getProfile()
  } else {
    setProfileData(getProfileData.value)
  }
  if (getJobPreferenceData.value === null) {
    getJobPreference()
  } else {
    setJobPrefData(getJobPreferenceData.value)
  }
  if (getUserInterestsData.value === null || getUserInterestsData.value.length === 0) {
    getUserInterests()
  } else {
    setInterestsData(getUserInterestsData.value)
  }
})

watch(getProfileData, (value) => {
  if (value) {
    setProfileData(value)
  }
})

watch(getJobPreferenceData, (value) => {
  if (value) {
    setJobPrefData(value)
  }
})

watch(getUserInterestsData, (value) => {
  if (value) {
    setInterestsData(value)
  }
})
</script>

<template>
  <main class="flex justify-content-center align-items-center flex-wrap w-screen">
    <div class="flex align-items-center justify-content-center font-bold border-round w-screen">
      <Card class="w-8 mt-5">
        <template #content>
          <div class="text-xl font-semibold text-center">Personal Information</div>
          <DataTable :value="profileData" table-style="min-width: 50rem" class="mt-5">
            <Column field="label" header="Field"></Column>
            <Column field="value" header="Value"></Column>
          </DataTable>
          <Divider />
          <div class="text-xl font-semibold text-center">Job Preference</div>
          <DataTable :value="jobPrefData" table-style="min-width: 50rem" class="mt-5">
            <Column field="label" header="Field"></Column>
            <Column field="value" header="Value"></Column>
          </DataTable>
          <Divider />
          <div class="text-xl font-semibold text-center">Your Interests</div>
          <div class="flex align-items-center justify-content-center mt-5 gap-2">
            <template v-for="(name, index) in interestsData" :key="index">
              <Chip :label="name" />
            </template>
          </div>
        </template>
      </Card>
    </div>
  </main>
</template>
