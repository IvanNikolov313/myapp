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
          path: 'screener-configs',
          name: 'ScreenerConfigs',
          component: () => import('../pages/ScreenerConfigs.vue'),
          meta: { requiresAuth: true }
        },
      ],
      
  },
  
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

// ✅ Global guard (frontend-only check)
router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('token')
  if (to.path.startsWith('/admin') && !token) {
    return next('/login')
  }
  next()
})

export default router
