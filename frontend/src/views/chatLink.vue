<template>
    <div class="container">
      <Error v-if="error_message" :message="error_message"></Error>
      <div class="row mt-5 d-flex justify-content-center align-items-center vh-50">
        <div class="col-12 col-md-8 col-lg-6 col-xl-5">
          <div class="card shadow">
            <div class="card-body text-center">
              <h3 class="mb-5">Add Gspace link</h3>
              <form @submit.prevent="updatelink()">
              <div class="form-outline mb-4">
              <input class="form-control form-control-lg" type="text" placeholder="Enter Google Space Bot Link Here"  v-model="info.link" />
              <label class="form-label">Google Space Bot Link</label>
              </div>
              <button class="btn btn-lg btn-secondary w-100" type="submit">Add Link</button>
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
    info:{link:""},
    error_message:null
  }
  },
  methods: {
    async updatelink(){
      this.error_message=null
      const response = await fetch("http://localhost:8080/api/link",
        {
            headers: {"Content-Type":"application/json","Authentication-Token":localStorage.getItem("token")},
            method: "post",
            body: JSON.stringify(this.info)
        }).catch(()=>this.error_message='Server is down')

        if(response){
        if(response.ok){
          const d = await response.json()
          this.$router.push({name:"dashboard"})
          }else{
            const e = await response.json()
            this.error_message=e.error_message
         }
        }
        }
    },
    mounted(){
      document.title="Chat Link"
    },
  components:{
    Error
  }
  
  }
</script>
