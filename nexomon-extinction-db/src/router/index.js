import { createRouter, createWebHashHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import NexomonList from '@/components/NexomonList.vue'
import NexomonDetails from '@/components/NexomonDetails'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: HomeView
  },
  {
    path: '/dex',
    name: 'Nexomon Database',
    component: NexomonList
  },
  {
    path: '/nexomon/:number',
    name: 'Nexomon Details',
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
  routes,
  scrollBehavior() {
    return { x: 0, y: 0 }; // Forces scroll to the top on each route
  }
})

router.beforeEach((to, from, next) => {
  document.title = to.name;
  next();
});

export default router
