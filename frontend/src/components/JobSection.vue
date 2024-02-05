<script setup>
import { ref } from 'vue'
import InputText from 'primevue/inputtext'
import Button from 'primevue/button'

const firstName = ref('')
const submitting = ref(false)

const submitPersonalInformation = async () => {}
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
