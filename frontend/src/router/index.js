import Vue from 'vue'
import VueRouter from 'vue-router'
import Home from '@/views/Home.vue'
import store from '@/store'

Vue.use(VueRouter)

const originalPush = VueRouter.prototype.push;
VueRouter.prototype.push = function push(location) {
  return originalPush.call(this, location).catch(err => err);
};

const routes = [
  {
    path: '/',
    name: 'home',
    component: Home,
    meta: {
      requireAuth: true
    },
    children: [
      {
        path: 'test',
        component: () => import(/* webpackChunkName: "Test" */ '@/views/test.vue'),
        meta: {
          requireAuth: true
        }
      }
    ]
  },
  {
    path: '/register',
    name: 'register',
    component: () => import(/* webpackChunkName: "Register" */ '@/views/auth/Register.vue')
  },
  {
    path: '/login',
    name: 'login',
    component: () => import(/* webpackChunkName: "Login" */ '@/views/auth/Login.vue')
  }
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

router.beforeEach((to, from, next) => {
  if (to.meta.requireAuth) { // 判断该路由是否需要登录权限
    if (localStorage.getItem('token')) {
      store.commit('setToken', { 'token': localStorage.getItem('token') })
    }
    if (store.state.token) { // 通过vuex state获取当前的token是否存在
      store.dispatch('getUserInfo').then(() => {
        next()
      })
    } else {
      next({
        path: '/login',
        query: { redirect: to.fullPath } // 将跳转的路由path作为参数，登录成功后跳转到该路由
      })
    }
  } else {
    next()
  }
})

router.afterEach(() => {
  window.scrollTo(0, 0)
})

export default router
