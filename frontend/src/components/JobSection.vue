<script setup>
import { nextTick, onMounted, ref, watch } from 'vue'
import Dropdown from 'primevue/dropdown'
import Button from 'primevue/button'
import Message from 'primevue/message'
import InputNumber from 'primevue/inputnumber'

import { useUserStore } from '@/store/user.js'
import { storeToRefs } from 'pinia'

const userStore = useUserStore()
const { getJobPreferenceData } = storeToRefs(userStore)
const { getJobPreference, updateJobPreference } = userStore

const experienceLevel = ref(null)
const expectedSalary = ref(null)
const submitting = ref(false)
const errorMessage = ref()

const experienceLevelOptions = ref([
  {
    label: 'Entry level',
    value: 1
  },
  {
    label: 'Manager',
    value: 2
  },
  {
    label: 'Other',
    value: 3
  }
])

const setFields = (jobPreferenceData) => {
  const { experience_level, expected_salary } = jobPreferenceData
  experienceLevel.value = experience_level
  if (expected_salary) {
    expectedSalary.value = parseFloat(expected_salary)
  }
}

watch(getJobPreferenceData, (jobPreferenceData) => {
  setFields(jobPreferenceData)
})

onMounted(() => {
  if (getJobPreferenceData.value === null) {
    getJobPreference()
  } else {
    setFields(getJobPreferenceData.value)
  }
})

const submitJobInformation = async () => {
  errorMessage.value = null
  if (experienceLevel.value === null || expectedSalary.value === null) {
    await nextTick(() => {
      errorMessage.value = ['Please input all required fields.']
    })
    return
  }
  submitting.value = true
  const { success, errors } = await updateJobPreference({
    experience_level: experienceLevel.value,
    expected_salary: expectedSalary.value
  })
  if (success) {
    submitting.value = false
  } else {
    if (errors) {
      errorMessage.value = errors
      submitting.value = false
    }
  }
}
</script>

<template>
  <transition-group name="p-message" tag="div">
    <Message v-for="(msg, index) in errorMessage" :key="index" severity="error">
      {{ msg }}
    </Message>
  </transition-group>
  <form @submit.prevent="submitting === false && submitJobInformation()">
    <div class="field">
      <label for="experience-level">Experience level</label>
      <Dropdown
        v-model="experienceLevel"
        :options="experienceLevelOptions"
        option-label="label"
        option-value="value"
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
      <label for="expected-salary">Expected salary</label>
      <InputNumber
        v-model="expectedSalary"
        input-id="minmaxfraction"
        :min-fraction-digits="0"
        :max-fraction-digits="2"
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
        label="Update Information"
        class="flex align-items-center justify-content-center"
      />
    </div>
  </form>
</template>

<style scoped></style>
