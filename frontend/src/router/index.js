import { createRouter, createWebHistory } from 'vue-router'
import Login from '../views/Login.vue'
import Dashboard from '../views/Dashboard.vue'
import Teams from '../views/Teams.vue'
import Players from '../views/Players.vue'
import Games from '../views/Games.vue'
import GameDetails from '../views/GameDetails.vue'
import PlayerGameDetails from '../views/PlayerGameDetails.vue'
import Rankings from '../views/Rankings.vue'
import Posts from '../views/Posts.vue'
import Query from '../views/Query.vue'
import Profile from '../views/Profile.vue'
import PlayerComparison from '../views/PlayerComparison.vue'
import PlayerDetails from '../views/PlayerDetails.vue'

const routes = [
  {
    path: '/',
    redirect: '/dashboard'
  },
  {
    path: '/login',
    name: 'Login',
    component: Login
  },
  {
    path: '/dashboard',
    name: 'Dashboard',
    component: Dashboard,
    meta: { requiresAuth: true }
  },
  {
    path: '/teams',
    name: 'Teams',
    component: Teams,
    meta: { requiresAuth: true }
  },
  {
    path: '/players',
    name: 'Players',
    component: Players,
    meta: { requiresAuth: true }
  },
  {
    path: '/players/:id',
    name: 'PlayerDetails',
    component: PlayerDetails,
    meta: { requiresAuth: true }
  },
  {
    path: '/comparison',
    name: 'PlayerComparison',
    component: PlayerComparison,
    meta: { requiresAuth: true }
  },
  {
    path: '/games',
    name: 'Games',
    component: Games,
    meta: { requiresAuth: true }
  },
  {
    path: '/games/:id',
    name: 'GameDetails',
    component: GameDetails,
    meta: { requiresAuth: true }
  },
  {
    path: '/games/:gameId/players/:playerId',
    name: 'PlayerGameDetails',
    component: PlayerGameDetails,
    meta: { requiresAuth: true }
  },
  {
    path: '/rankings',
    name: 'Rankings',
    component: Rankings,
    meta: { requiresAuth: true }
  },
  {
    path: '/posts',
    name: 'Posts',
    component: Posts,
    meta: { requiresAuth: true }
  },
  {
    path: '/query',
    name: 'Query',
    component: Query,
    meta: { requiresAuth: true, requiresAnalyst: true }
  },
  {
    path: '/profile',
    name: 'Profile',
    component: Profile,
    meta: { requiresAuth: true }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('token')
  const user = JSON.parse(localStorage.getItem('user') || '{}')
  
  if (to.meta.requiresAuth && !token) {
    next('/login')
  } else if (to.meta.requiresAnalyst && user.role !== 'analyst' && user.role !== 'admin') {
    next('/dashboard')
  } else {
    next()
  }
})

export default router