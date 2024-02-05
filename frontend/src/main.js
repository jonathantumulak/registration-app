import './assets/main.css'

import { createApp } from 'vue'
import App from './App.vue'
import router from './router'

// extra apps
import PrimeVue from 'primevue/config'
import 'primevue/resources/themes/aura-light-green/theme.css'
import 'primeflex/primeflex.css'
import 'primeicons/primeicons.css'
import { createPinia } from 'pinia'

const app = createApp(App)
const pinia = createPinia()

app.use(router)
app.use(PrimeVue)
app.use(pinia)

app.mount('#app')
