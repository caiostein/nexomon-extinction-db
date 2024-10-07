import { createRouter, createWebHashHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import NexomonList from '@/components/NexomonList.vue'
import NexomonDetails from '@/components/NexomonDetails'

const routes = [
  {
    path: '/',
    name: 'home',
    component: HomeView
  },
  {
    path: '/dex',
    name: 'dex',
    component: NexomonList
  },
  {
    path: '/nexomon/:number',
    name: 'NexomonDetails',
    component: NexomonDetails, // Nexomon details page
    props: true, // Allow route params as props
  },
  {
    path: '/about',
    name: 'about',
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () => import(/* webpackChunkName: "about" */ '../views/AboutView.vue')
  }
]

const router = createRouter({
  history: createWebHashHistory(),
  routes
})

export default router
