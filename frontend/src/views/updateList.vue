<template>
  <div class="container">
    <Error v-if="error_message" :message="error_message"></Error>
    <div class="row mt-5 d-flex justify-content-center align-items-center vh-50">
      <div class="col-12 col-md-8 col-lg-6 col-xl-5">
        <div class="card shadow">
          <div class="card-body text-center">
            <h3 class="mb-5">Update List</h3>
            <form @submit.prevent="updatelist(listInfo)">
            <div class="form-outline mb-4">
            <input class="form-control form-control-lg" type="name" placeholder="Enter List Name" v-model="listInfo.name" />
            <label class="form-label">List Name</label>
            </div>
            <button class="btn btn-lg btn-secondary w-100" type="submit">Update List</button>
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
    listInfo: {
    name: null
  },list_id:null,
  error_message:null
  }
  },
  methods: {
    async updatelist(listInfo){
      this.error_message=null
      const response = await fetch("http://localhost:8080/api/list",
        {
            headers: {"Content-Type":"application/json","Authentication-Token":localStorage.getItem("token")},
            method: "put",
            body: JSON.stringify(listInfo)
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
  mounted() {document.title="Update List"
  this.list_id=this.$route.params.list_id;
  if(this.list_id){
    fetch(`http://localhost:8080/api/list/${this.list_id}`,
        {
            headers: {"Content-Type":"application/json","Authentication-Token":localStorage.getItem("token")},
            method: "get"
        }).then(r=> r.json()).then(d=>this.listInfo=d).catch(e=>console.log(e))
    }else{
        this.$router.push({name:"dashboard"})
    }
  },
  components:{
    Error
  }
}
</script>
  
  <style scoped>
  
  </style>