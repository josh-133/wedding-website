import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '../stores/auth'

const routes = [
  {
    path: '/',
    name: 'home',
    component: () => import('../views/HomePage.vue'),
  },
  {
    path: '/engagement',
    name: 'engagement',
    component: () => import('../views/EngagementRsvpPage.vue'),
  },
  {
    path: '/wedding',
    name: 'wedding',
    component: () => import('../views/WeddingRsvpPage.vue'),
  },
  {
    path: '/registry',
    name: 'registry',
    component: () => import('../views/RegistryPage.vue'),
  },
  {
    path: '/admin',
    name: 'admin-login',
    component: () => import('../views/AdminLoginPage.vue'),
  },
  {
    path: '/admin/dashboard',
    name: 'admin-dashboard',
    component: () => import('../views/AdminDashboardPage.vue'),
    meta: { requiresAuth: true },
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

router.beforeEach((to, from, next) => {
  if (to.meta.requiresAuth) {
    const authStore = useAuthStore()
    if (!authStore.isAuthenticated) {
      next({ name: 'admin-login' })
      return
    }
  }
  next()
})

export default router
