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
    {
      path: '/translation',
      name: 'translation',
      component: () => import('@/pages/TranslationPage.vue'),
    },
    {
      path: '/compliance',
      name: 'compliance',
      component: () => import('@/pages/CompliancePage.vue'),
    },
    {
      path: '/optimization',
      name: 'optimization',
      component: () => import('@/pages/OptimizationPage.vue'),
    },
    {
      path: '/research',
      name: 'research',
      component: () => import('@/pages/ResearchPage.vue'),
    },
  ],
})

export default router
