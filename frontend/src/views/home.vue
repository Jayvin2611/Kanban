<template>
  <div class="container">    <Error v-if="error_message" :message="error_message"></Error>
    <div class="row mt-5 d-flex justify-content-center align-items-center vh-50">
      <div class="col-12 col-md-8 col-lg-6 col-xl-5">
        <div class="card shadow">
          <div class="card-body text-center">
            <h3 class="mb-5">Login</h3>
            <form @submit.prevent="LoginUser(userInfo)">
              <div class="form-outline mb-4">
                <input class="form-control form-control-lg" type="email" placeholder="Enter Email" v-model="userInfo.email" />
                <label class="form-label">Email</label>
              </div>
              <div class="form-outline mb-4">
                <input class="form-control form-control-lg" type="password" placeholder="Enter Password" v-model="userInfo.password" />
                <label class="text-right">Password</label>
              </div>
              <button class="btn btn-lg btn-secondary w-100" type="submit"> Login </button><br />
            </form>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>


<script>
import Error from "../components/Error.vue"

export default {
  data() {
    return {
      userInfo: {
      email: null,
      password: null,
      },
    error_message:null
    }
  },
  methods: {
    async LoginUser(user){
      this.error_message=null
      const response = await fetch("http://localhost:8080/login?include_auth_token",{headers: {"Content-Type":"application/json"},
                      method: "post",
                      body: JSON.stringify(user)}).catch(()=>this.error_message='Server is down')
      if(response){
        if(response.ok){
          const d = await response.json()
          localStorage.setItem('token',d.response.user.authentication_token)
          this.$router.push({name:'dashboard'})
        }else{
          const e = await response.json()
          this.error_message=e.response.errors[0]
        }
      }
    }
  },
  mounted() {
    document.title="Home"
  },
  components:{
    Error
  }
}
</script>