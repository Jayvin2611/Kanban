<template>
<div>
  <Error v-if="error_message" :message="error_message"></Error>
  <div class="container">
    <div class="row mt-5 d-flex justify-content-center align-items-center vh-50">
      <div class="col-12 col-md-8 col-lg-6 col-xl-5">
        <div class="card shadow">
          <div class="card-body text-center">
            <h3 class="mb-5">Signup</h3>
            <form @submit.prevent="SignupUser(userInfo)">
            <div class="form-outline mb-4">
            <input class="form-control form-control-lg" type='text' placeholder='Enter First Name' v-model='userInfo.first_name' />
            </div>
            <div class="form-outline mb-4">
            <input class="form-control form-control-lg" type='text' placeholder='Enter Last Name' v-model='userInfo.last_name' />
            </div>
            <div class="form-outline mb-4">
            <input class="form-control form-control-lg" type='email' placeholder='Enter Email' v-model='userInfo.email' />
            </div>
            <div class="form-outline mb-4">
            <input class="form-control form-control-lg" type='password' placeholder='Enter Password' v-model='userInfo.password' />
            </div>
            <button class="btn btn-secondary btn-lg w-100" type="submit"> Signup </button>
            </form>
          </div>
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
        first_name: null,
        last_name: null
      },
      error_message:null
    }
  },
  components:{
    Error
  },
  methods: {
    async SignupUser(user){
      this.error_message=null
      const response = await fetch('http://localhost:8080/api/user',{headers: {"Content-Type":"application/json"},
      method: "post",
      body: JSON.stringify(user)}).catch(()=>this.error_message='Server is down')
      
      if(response){
        if(response.ok){
          const d = await response.json()
          localStorage.setItem('token',d.token)
          this.$router.push({name:'dashboard'})
        }else{
          const e = await response.json()
          this.error_message=e.error_message
        }
      }
    }
  },
  mounted() {
      document.title='Sign Up'
  }
}
</script>

<style scoped>
</style>