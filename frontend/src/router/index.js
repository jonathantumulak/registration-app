import { createRouter, createWebHistory } from 'vue-router'
import { useUserStore } from '@/store/user'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: () => import('../views/HomeView.vue')
    },
    {
      path: '/login',
      name: 'login',
      props: true,
      component: () => import('../views/LoginView.vue')
    },
    {
      path: '/register',
      name: 'register',
      component: () => import('../views/RegisterView.vue')
    },
    {
      path: '/welcome',
      name: 'welcome',
      component: () => import('../views/WelcomeView.vue')
    }
  ]
})

router.beforeEach(async (to) => {
  const userStore = useUserStore()
  const { userIsAuthenticated } = userStore

  const userAuthenticated = await userIsAuthenticated()

  if (userAuthenticated && ['login', 'register'].includes(to.name)) {
    return { name: 'home' }
  } else if (!userAuthenticated && !['login', 'register'].includes(to.name)) {
    return { name: 'login' }
  }
})

export default router
