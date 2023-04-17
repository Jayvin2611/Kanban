import Vue from 'vue'
import VueRouter from 'vue-router'
import Home from '../views/home.vue'

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    name: 'home',
    component: Home,
    alias: '/login'
  },
  {
    path: '/signup',
    name: 'sign-up',
    component: function () {
      return import('../views/signUp.vue')
    }
  },
  {
    path: '/dashboard',
    name: 'dashboard',
    component: function () {
      return import('../views/dashboard.vue')
    }
  },
  {
    path: '/addlist',
    name: 'addlist',
    component: function () {
      return import('../views/addList.vue')
    }
  },
  {
    path: '/addcard/',
    name: 'addcard',
    component: function () {
      return import('../views/addCard.vue')
    },
    props: true
  },
  {
    path: '/updatelist/',
    name: 'updatelist',
    component: function () {
      return import('../views/updateList.vue')
    },
    props: true
  },
  {
    path: '/updatecard/',
    name: 'updatecard',
    component: function () {
      return import('../views/updateCard.vue')
    },
    props: true
  },
  {
    path: '/summary',
    name: 'summary',
    component: function () {
      return import('../views/summary.vue')
    }
  },
  {
    path: '/user',
    name: 'user',
    component: function () {
      return import('../views/userDetails.vue')
    }
  },
  {
    path: '/chat',
    name: 'chat',
    component: function () {
      return import('../views/chatLink.vue')
    }
  }
]

const router = new VueRouter({
  routes
})

router.beforeEach((to, from,next)=>{
  if((to.name==='home' || to.name==='sign-up')){
    if(localStorage.getItem('token')){
          next({name:'dashboard'})
      }else{
          next()
      }
    }
    else{
      if(localStorage.getItem('token')){
        next()
      }else{
      next({name:'home'})
      }
    }
})

export default router
