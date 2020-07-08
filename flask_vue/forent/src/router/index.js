import Vue from 'vue'
import Router from 'vue-router'
import Home from '@/components/Home'
import Login from '@/components/Login'
import Register from '@/components/Register'
import Profile from '@/components/Profile'
import Ping from '@/components/Ping'

Vue.use(Router)

const router = new Router({
  routes: [
    {
      path: '/',
      name: 'Home',
      component: Home,
      meta: {
        requiresAuth:true
      }
    },
    {
      path: '/login',
      name: 'Login',
      component:Login,
    },
    {
      path: '/register',
      name: '/Register',
      component: Register,
    },
    {
      path: '/profile',
      name: 'Profile',
      component: Profile,
      meta: {
        requiresAuth: true   //  这个值设置为true 代表需要身份验证。
      }
    },
    {
      path: '/ping',
      name: 'Ping',
      component: Ping
    }
  ]
})


/* 只有用户登录后才能访问 Home、Profile 等，需要使用 Vue-Router 的 router.beforeEach() 在每次路由前判断是否需要用户验证 */

router.beforeEach((to, from, next) => {
  const token = window.localStorage.getItem('user-token') // 去localStorage找token，若token不存在则表示用户无认证，去登录请求token。
  if (to.matched.some(record => record.meta.requiresAuth) && (!token || token === null)){ // 判断是否requiresAuth为true并且没有携带token。
    next({
      path: '/login',
      query: { redirect: to.fullPath }
    })
  } else if (token && to.name == 'Login') {
    // 用户已经登陆， 再次访问登陆界面，不让进入页面。
    next({
      path: from.fullPath
    })
  } else {
    next()
  }
})

export default router