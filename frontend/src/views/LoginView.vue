<script setup>
  import { RouterLink } from 'vue-router'
  import Card from 'primevue/card';
  import InputText from 'primevue/inputtext';
  import Button from 'primevue/button';
  import Divider from 'primevue/divider';
  import Password from 'primevue/password';

  import { ref } from 'vue';

  let username = ref();
  let password = ref();

</script>

<template>
    <main class="flex justify-content-center align-items-center flex-wrap h-30rem">
      <div class="flex align-items-center justify-content-center font-bold border-round">
        <Card>
          <template #title>Login</template>
          <template #content>
            <div class="field">
              <label for="firstname1">Username</label>
              <InputText
                v-model="username"
                type="text"
                class="text-base text-color surface-overlay p-2 border-1 border-solid surface-border border-round appearance-none outline-none focus:border-primary w-full"
              />
            </div>
            <div class="field">
              <label for="lastname1">Password</label>
              <Password
                v-model="password"
                :feedback="false"
                class="w-full"
                :pt="{
                  input: {
                    root: {
                     class: ['w-full']
                    }
                  },
                }"
              />
            </div>
            <div class="flex justify-content-end flex-wrap">
              <Button
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
          </template>
        </Card>
      </div>
    </main>
</template>


<style scoped>
</style>
