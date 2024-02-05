import './assets/main.css'

import { createApp } from 'vue'
import App from './App.vue'
import router from './router'

// extra apps
import PrimeVue from 'primevue/config'
import 'primevue/resources/themes/aura-light-green/theme.css'
import 'primeflex/primeflex.css'
import 'primeicons/primeicons.css'
import axios from 'axios'
import VueAxios from 'vue-axios'
import { createPinia } from 'pinia'

const app = createApp(App)

app.use(router)

app.use(PrimeVue)
app.use(VueAxios)
app.use(axios)
const pinia = createPinia()
app.use(pinia)

app.mount('#app')
