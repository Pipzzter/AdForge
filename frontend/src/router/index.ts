import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: () => import('@/pages/HomePage.vue'),
    },
    {
      path: '/copyinjection',
      name: 'copyinjection',
      component: () => import('@/pages/CopyInjectionPage.vue'),
    },
  ],
})

export default router
