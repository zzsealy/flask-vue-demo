<template>
  <div style="margin: 10% 40%; border: 1px solid black; text-align: center">
    <alert 
      v-if="sharedState.is_new"
      v-bind:variant="alertVariant"
      v-bind:message="alertMessage">
    </alert>
    <h1>登陆</h1>
    <div class="row">
      <div class="col-md-4">
        <form @submit.prevent="onSubmit">
            <div style="margin-left:80%; width:200px">
            <label for="username">用户名</label>
            <input type="text" v-model="loginForm.username" class="form-control" v-bind:class="{'is-invalid': loginForm.usernameError}" id="username" placeholder="">
            <div v-show="loginForm.usernameError" class="invalid-feedback">{{ loginForm.usernameError }}</div>
          
          
            <label for="password">密码</label>
            <input type="password" v-model="loginForm.password" class="form-control" v-bind:class="{'is-invalid': loginForm.passwordError}" id="password" placeholder="">
            <div v-show="loginForm.passwordError" class="invalid-feedback">{{ loginForm.passwordError }}</div>
            </div>
          <button type="submit" style="margin-left: 140px; width:100px; margin-top:15px" class="btn btn-primary">登陆</button>
        </form>
      </div>
    </div>
    <br>
    <p>新用户？ <router-link to="/register">注册用户!</router-link></p>
    <p>
        忘记密码？
        <a href="#">重置密码！</a>
    </p>
  </div>
</template>

<script>
import axios from 'axios'
import Alert from './Alert'
import store from '../store.js'

export default {
  name: 'Login',  //this is the name of the component
  components: {
    alert: Alert
  },
  data () {
    return {
      sharedState: store.state,
      alertVariant: 'info',
      alertMessage: 'Congratulations, you are now a registered user !',
      loginForm: {
        username: '',
        password: '',
        submitted: false,  // 是否点击了 submit 按钮
        errors: 0,  // 表单是否在前端验证通过，0 表示没有错误，验证通过
        usernameError: null,
        passwordError: null
      }
    }
  },
  methods: {
    onSubmit (e) {
      this.loginForm.submitted = true  // 先更新状态
      this.loginForm.errors = 0

      if (!this.loginForm.username) {
        this.loginForm.errors++
        this.loginForm.usernameError = 'Username required.'
      } else {
        this.loginForm.usernameError = null
      }

      if (!this.loginForm.password) {
        this.loginForm.errors++
        this.loginForm.passwordError = 'Password required.'
      } else {
        this.loginForm.passwordError = null
      }

      if (this.loginForm.errors > 0) {
        // 表单验证没通过时，不继续往下执行，即不会通过 axios 调用后端API
        return false
      }

      const path = '/tokens'
      // axios 实现Basic Auth需要在config中设置 auth 这个属性即可
      this.$axios.post(path, {}, {
        auth: {
          'username': this.loginForm.username,
          'password': this.loginForm.password
        }
      }).then((response) => {
          // handle success
          window.localStorage.setItem('user-token', response.data.token)
          store.loginAction()
          
          const name = JSON.parse(atob(response.data.token.split('.')[1])).name
          this.$toasted.success(`Welcome ${name}!`, { icon: 'fingerprint' })

          if (typeof this.$route.query.redirect == 'undefined') {
            this.$router.push('/')
          } else {
            this.$router.push(this.$route.query.redirect)
          }
        })
        .catch((error) => {
          // handle error
          console.log(error.response);
        })
    }
  }
}
</script>