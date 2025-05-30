import { createRouter, createWebHashHistory } from 'vue-router'
import NexomonList from '@/components/NexomonList.vue'
import NexomonDetails from '@/components/NexomonDetails'
import LocationList from '@/components/LocationList.vue'
import LocationDetails from '@/components/LocationDetails.vue'
import SkillList from '@/components/SkillList.vue'

const routes = [
  {
    path: '/',
    redirect: '/nexomons'
  },
  {
    path: '/nexomons',
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
    path: '/locations',
    name: 'Location Database',
    component: LocationList
  },
  {
    path: '/location/:location',
    name: 'Location Details',
    component: LocationDetails,
    props: true
  },
  {
    path: '/skills',
    name: 'Skill Database',
    component: SkillList
  },
  {
    path: '/skill/:skillName',
    name: 'Skill Details',
    component: () => import('../components/SkillDetails.vue'),
    props: true
  },
  {
    path: '/collection',
    name: 'My Collection',
    component: () => import('../components/CollectionList.vue')
  },
  {
    path: '/about',
    name: 'About',
    component: () => import('../views/AboutView.vue')
  }
]

const router = createRouter({
  history: createWebHashHistory(),
  routes,
  scrollBehavior() {
    return new Promise((resolve) => {
      setTimeout(() => {
        resolve({ left: 0, top: 0 });
      }, 50);
    });
  }
})

router.beforeEach((to, from, next) => {
  // Store the previous route in localStorage for smarter navigation
  localStorage.setItem('previousRoute', JSON.stringify({
    name: from.name,
    path: from.path,
    params: from.params
  }));
  
  document.title = to.name;
  next();
});

export default router
