<template>
    <div class="container">
    <h1>Edit Your Profile</h1>
    <div class="row">
      <div class="col-md-4">
        <form @submit.prevent="onSubmit">
          <div class="form-group">
            <label for="name">真实姓名</label>
            <input type="text" v-model="profileForm.name" class="form-control" id="name" placeholder="">
          </div>
          <div class="form-group">
            <label for="location">住址</label>
            <input type="text" v-model="profileForm.location" class="form-control" id="location" placeholder="">
          </div>
          <div class="form-group">
            <label for="about_me">关于我</label>
            <textarea v-model="profileForm.about_me" class="form-control" id="about_me" rows="5" placeholder=""></textarea>
          </div>
          <button type="submit" class="btn btn-primary">Submit</button>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import store from '../store.js'
export default {
    name: 'EditProfile', // 组件名称
    data() {
        return {
        sharedState: store.state,
        profileForm: {
            name: '',
            location: '',
            about_me: '',
            submitted: false // 是否点击了提交按钮
        }
       }
    },
    methods: {
        getUser(id) {
            const path = `/users/${id}`
            this.$axios.get(path)
                .then((response) => {
                    console.log(response)
                    this.profileForm.name = response.data.name
                    this.profileForm.location = response.data.location
                    this.profileForm.about_me = response.data.about_me
                })
                .catch((error) => {
                    console.error(error)
                });
        },
        onSubmit(e) {
            const user_id = this.sharedState.user_id
            const path = `/users/${user_id}`
            const payload = {
                name: this.profileForm.name,
                location: this.profileForm.location,
                about_me: this.profileForm.about_me
            }
            this.$axios.put(path, payload)
                .then((response) => {
                    console.log(response)
                    this.$toasted.success("修改用户信息成功.", { icon: 'fingerprint'})
                    this.$router.push({
                        name: 'Profile',
                        params: {id: user_id}
                    })
                })
                .catch((error) => {
                    console.error(error.response.data)
                })
        },
    },
    created() {
        const user_id = this.sharedState.user_id
        this.getUser(user_id)
    }
}
</script>