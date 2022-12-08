import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView'

const routes = [
  {
    path: '/',
    name: 'home',
    component: HomeView
  },
  {
    path: '/linear_regression',
    name: 'Linear Regression Model',
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () => import(/* webpackChunkName: "LR" */ '../views/LRView')
  },
  {
    path: '/logistic_regression',
    name: 'Logistic Regression Model',
    component: () => import(/* webpackChunkName: "LGR" */ '../views/LGRView')
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
