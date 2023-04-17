<template>
  <div class="container">
    <Error v-if="error_message" :message="error_message"></Error>
    <div class="row mt-5 d-flex justify-content-center align-items-center vh-50">
      <div class="col-12 col-md-8 col-lg-6 col-xl-5">
        <div class="card shadow">
          <div class="card-body text-center">
            <h3 class="mb-5">Add Card</h3>
            <form @submit.prevent="addcard(cardInfo)">
            <div class="form-outline mb-4">
            <input class="form-control form-control-lg" type="text" placeholder="Enter Card Title" v-model="cardInfo.title" required />
            </div>
            <div class="form-outline mb-4">
            <input class="form-control form-control-lg" type="text" placeholder="Enter Card Content" v-model="cardInfo.content"/>
            </div>
            <div class="form-outline mb-4">
            <input class="form-control form-control-lg" type="datetime-local" v-model="cardInfo.deadline" required/><br>
            </div>
            <div class="form-outline mb-4">
              <label class="form-check-label m-3" >Complete Status :</label><br>
            <input class="form-check-input" type="radio"  v-model="cardInfo.completed" v-bind:value=true>
            <label class="form-check-label me-4" >Complete</label>
            <input class="form-check-input" type="radio"  v-model="cardInfo.completed" v-bind:value=false>
            <label class="form-check-label" >Pending</label>
            </div>
            <button class="btn btn-lg btn-secondary w-100"  type="submit"> Add Card </button><br />
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
  cardInfo: {
    list_id: null,
    title : null,
    content : null,
    deadline : null,
    completed : null
  },
  error_message:null
  }
  },
  methods: {
    async addcard(cardInfo){
      this.error_message=null
      const response = await fetch("http://localhost:8080/api/card",
        {
            headers: {"Content-Type":"application/json","Authentication-Token":localStorage.getItem("token")},
            method: "post",
            body: JSON.stringify(cardInfo)
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
  mounted() {document.title="Add Card";
            this.cardInfo.list_id=this.$route.params.list_id
            if(!this.cardInfo.list_id){
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