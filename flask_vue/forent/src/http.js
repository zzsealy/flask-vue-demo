// 前端如果每次通过 axios 调用后端 API 时，指定的 API URL都写死到各个组件中，
// 现在开发环境是类似 http://localhost:5000/api/users/1 这样的，
// 如果后续部署到生产环境上，可能IP和端口会变动，所以可以通过 axios 全局配置一次指定

import Vue from 'vue'
import axios from 'axios'
import store from './store'
import router from './router'

// 基础配置
axios.defaults.timeout = 5000 // 超时时间
axios.defaults.baseURL = 'http://localhost:5000/api'

// 用户以后访问后端需要认证的 API 时都要传输 Token，而 axios 可以通过创建 request interceptor 自动帮你添加 Token 到请求头 Authorization 中。
// 添加 request interceptor
axios.interceptors.request.use(function(config) {
// 添加请求发送前的操作(Do something before request is sent).
    const token = window.localStorage.getItem("user-token")
    if(token) {
        config.headers.Authorization = `Bearer ${token}`
    }
    return config
}, function(error) {
    // Do something with request error.
    return Promise.reject(error)
})

/*
JWT的有效期要设置的短一些，当它过期后，用户再通过它访问后端 API 时会返回 401 UNAUTHORIZED 错误，
让 axios 自动处理这个错误，如果用户当前访问的不是 /login 路由（正常登录）时，会自动跳转到登录页，要求用户重新认证
*/

// 增加请求拦截器 respon interceptor
axios.interceptors.response.use(function(response) {
    // Do something with response data
    return response
}, function(error) {
    // Do something with response error
    switch (error.response.status) {
        case 401:
            // 清除Token 以及 认证等状态
            store.logoutAction()
            // 跳转到登陆页面
            if (router.currentRoute.path !== '/login') {
                Vue.toasted.error('401: 认证已失效， 请重新登录', { icon: 'fingerprint'})
                router.replace({
                    path: '/login',
                    query: { redirect: router.currentRoute.path },
                })
            }
            break
        case 404:
            Vue.toasted.error('404: NOT FOUND', { icon: 'fingerprint' })
            router.back()
            break
    }
    return Promise.reject(error)
})

export default axios
