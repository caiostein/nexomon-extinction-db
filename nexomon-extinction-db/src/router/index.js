import { createRouter, createWebHashHistory } from 'vue-router'
import NexomonList from '@/components/NexomonList.vue'
import NexomonDetails from '@/components/NexomonDetails'

const routes = [
  {
    path: '/',
    name: 'Nexomon Database',
    component: NexomonList
  },
  {
    path: '/nexomon/:number',
    name: 'Nexomon Details',
    component: NexomonDetails,
    props: true,
  },
  {
    path: '/about',
    name: 'about',
    component: () => import('../views/AboutView.vue')
  }
]

const router = createRouter({
  history: createWebHashHistory(),
  routes,
  scrollBehavior() {
    return { x: 0, y: 0 };
  }
})

router.beforeEach((to, from, next) => {
  document.title = to.name;
  next();
});

export default router
