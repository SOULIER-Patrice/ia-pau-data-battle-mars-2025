import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeViews/HomeView.vue'
import { useAuthStore } from '@/stores/authStore'

const authRequired = (to: any, from: any, next: any) => {
  const authStore = useAuthStore()

  if (authStore.token) {
    next()
  } else {
    next({ name: 'login', query: { redirect: to.fullPath } })
  }
}

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView
    },
    {
      path: '/login',
      name: 'login',
      component: () => import('../views/LoginView.vue')
    },
    {
      path: '/profile',
      name: 'profile',
      beforeEnter: authRequired,
      component: () => import('../views/ProfileView.vue')
    },
    {
      path: '/practice',
      name: 'practice',
      beforeEnter: authRequired,
      component: () => import('../views/PracticesViews/SelectModeView.vue')
    },
    {
      path: '/practice/chat',
      name: 'chat',
      beforeEnter: authRequired,
      component: () => import('../views/PracticesViews/ChatView.vue')
    },
    {
      path: '/practice/MCQ',
      name: 'MCQ',
      beforeEnter: authRequired,
      component: () => import('../views/PracticesViews/ChatView.vue')
    },
    {
      path: '/about',
      name: 'about',
      // route level code-splitting
      // this generates a separate chunk (About.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () => import('../views/AboutView.vue')
    },
    {
      path: '/error',
      name: 'error',
      component: () => import('../views/ErrorView.vue')
    }
  ]
})

export default router
