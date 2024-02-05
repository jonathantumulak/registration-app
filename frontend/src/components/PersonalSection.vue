<script setup>
import { ref, watch, onMounted, nextTick } from 'vue'
import InputText from 'primevue/inputtext'
import Calendar from 'primevue/calendar'
import Button from 'primevue/button'
import Dropdown from 'primevue/dropdown'
import { useUserStore } from '@/store/user.js'
import { storeToRefs } from 'pinia'

const userStore = useUserStore()
const { getProfileData } = storeToRefs(userStore)
const { getProfile, updateProfile } = userStore

const firstName = ref('')
const lastName = ref('')
const birthDate = ref('')
const genderField = ref('')
const submitting = ref(false)
const errorMessage = ref()

const genderOptions = ref([
  {
    label: 'Male',
    value: 1
  },
  {
    label: 'Female',
    value: 2
  },
  {
    label: 'Other',
    value: 3
  }
])

const setFields = (profileData) => {
  const { first_name, last_name, birth_date, gender } = profileData
  firstName.value = first_name
  lastName.value = last_name
  birthDate.value = birth_date || ''
  genderField.value = gender || ''
}

watch(getProfileData, (profileData) => {
  setFields(profileData)
})

onMounted(() => {
  if (getProfileData.value === null) {
    getProfile()
  } else {
    setFields(getProfileData.value)
  }
})

const submitPersonalInformation = async () => {
  errorMessage.value = null
  if (
    firstName.value === '' ||
    lastName.value === '' ||
    birthDate.value === '' ||
    genderField.value === ''
  ) {
    await nextTick(() => {
      errorMessage.value = ['Please input all required fields.']
    })
    return
  }
  submitting.value = true
  const { success, errors } = await updateProfile({
    first_name: firstName.value,
    last_name: lastName.value,
    birth_date: birthDate.value,
    gender: genderField.value
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
  <form @submit.prevent="submitting === false && submitPersonalInformation()">
    <div class="field">
      <label for="firstname">First Name</label>
      <InputText
        v-model="firstName"
        type="text"
        name="firstname"
        class="text-base text-color surface-overlay p-2 border-1 border-solid surface-border border-round appearance-none outline-none focus:border-primary w-full"
      />
    </div>
    <div class="field">
      <label for="lastname">Last Name</label>
      <InputText
        v-model="lastName"
        type="text"
        name="lastname"
        class="text-base text-color surface-overlay p-2 border-1 border-solid surface-border border-round appearance-none outline-none focus:border-primary w-full"
      />
    </div>
    <div class="field">
      <label for="birthdate">Birth Date</label>
      <Calendar
        v-model="birthDate"
        date-format="yy/mm/dd"
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
      <label for="gender">Gender</label>
      <Dropdown
        v-model="genderField"
        :options="genderOptions"
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
