// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App'
import router from './router'
import VueToasted from 'vue-toasted'
import moment from 'moment'

// 导入配置了全局拦截器后的 axios
import axios from './http'
import 'bootstrap/dist/css/bootstrap.css'

Vue.config.productionTip = false

Vue.use(VueToasted, {
  // 主题样式 primary/outline/bubble
  theme: 'bubble',
  // 显示在页面哪个位置
  position: 'top-center',
  // 显示多久时间（毫秒)
  duration:3000,
  // 支持哪个图标集合。
  iconPack: 'material', // set your iconPack, defaults to material. material|fontawesome|custom-class
  // 可以执行那些动作
  action: {
    text: 'Cancel',
    onClick: (e, toastObject) => {
      toastObject.goAway(0)
    }
  },
});




// 将 $axios 挂载到 prototype 上， 在组件中可以直接使用 this.$axios 访问。
Vue.prototype.$axios = axios

// 将 moment挂载到 prototype 上， 在组件中使用 this.$moment 访问。
Vue.prototype.$moment = moment

/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  components: { App },
  template: '<App/>'
})
