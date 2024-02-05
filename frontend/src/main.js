import './assets/main.css'

import { createApp } from 'vue'
import App from './App.vue'
import router from './router'

// extra apps
import PrimeVue from 'primevue/config';
import 'primevue/resources/themes/aura-light-green/theme.css'

const app = createApp(App)

app.use(router)

app.use(PrimeVue);

app.mount('#app')
