import { createRouter, createWebHistory } from 'vue-router'
import Home from '@/views/Home.vue'
import ProductSearch from '@/views/ProductSearch.vue'
import ProductManagement from '@/views/ProductManagement.vue'
import UserInteraction from '@/views/UserInteraction.vue'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home
  },
  {
    path: '/product-search',
    name: 'ProductSearch',
    component: ProductSearch
  },
  {
    path: '/product-management',
    name: 'ProductManagement',
    component: ProductManagement
  },
  {
    path: '/user-interaction',
    name: 'UserInteraction',
    component: UserInteraction
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
