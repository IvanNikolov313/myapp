import { createRouter, createWebHistory } from 'vue-router'
import Login from '../pages/Login.vue'
import AdminLayout from '../pages/AdminLayout.vue'
import Dashboard from '../pages/Dashboard.vue'
import Settings from '../pages/Settings.vue'

const routes = [
  { path: '/', redirect: '/login' },
  { path: '/login', component: Login },
  {
    path: '/admin',
    component: AdminLayout,
    beforeEnter: (to, from, next) => {
      const token = localStorage.getItem('token')
      if (!token) return next('/login')
      next()
    },
    children: [
      { path: 'dashboard', component: Dashboard },
      { path: 'settings', component: Settings },
      {
        path: 'usa-dashboard',
        name: 'USADashboard',
        component: () => import('../pages/USADashboard.vue'),
        meta: { requiresAuth: true }
      },
      {
        path: 'usa-scrapes',
        name: 'USAScrapes',
        component: () => import('../pages/USAScrapes.vue'),
        meta: { requiresAuth: true }
      },
      {
        path: 'usa-screener-configs',
        name: 'USAScreenerConfigs',
        component: () => import('../pages/USAScreenerConfigs.vue'),
        meta: { requiresAuth: true },
      },
    ],
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

// Optional: Global guard
router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('token')
  if (to.path.startsWith('/admin') && !token) {
    return next('/login')
  }
  next()
})

export default router
