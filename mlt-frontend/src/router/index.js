import { createRouter, createWebHashHistory } from 'vue-router'
import HomeView from '../views/HomeView'

const routes = [
  {
    path: '/',
    name: 'home',
    component: HomeView
  },
  {
    path: '/LR',
    name: 'Linear Regression Model',
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () => import(/* webpackChunkName: "about" */ '../views/LRView')
  }
]

const router = createRouter({
  history: createWebHashHistory(),
  routes
})

export default router
