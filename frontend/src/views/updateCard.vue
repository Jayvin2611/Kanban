<template>
  <div class="container">
    <Error v-if="error_message" :message="error_message"></Error>
    <div class="row mt-5 d-flex justify-content-center align-items-center vh-50">
      <div class="col-12 col-md-8 col-lg-6 col-xl-5">
        <div class="card">
          <div class="card-body text-center">
            <h3 class="mb-5">Update Card</h3>
            <form @submit.prevent="updatecard(cardInfo)">
            <div class="form-outline mb-4">
            <input class="form-control form-control-lg" type="text" placeholder="Enter Card Title" v-model="cardInfo.title" />
            </div>
            <div class="form-outline mb-4">
            <input class="form-control form-control-lg" type="text" placeholder="Enter Card Content" v-model="cardInfo.content" />
            </div>
            <div class="form-outline mb-4">
            <input class="form-control form-control-lg" type="datetime-local" v-model="cardInfo.deadline" disabled /><br>
            </div>
            <div class="form-outline mb-4">
              <label class="form-check-label m-3" >Complete Status :</label><br>
            <input class="form-check-input" type="radio"  v-model="cardInfo.completed" v-bind:value=true>
            <label class="form-check-label me-4" >Complete</label>
            <input class="form-check-input" type="radio"  v-model="cardInfo.completed" v-bind:value=false>
            <label class="form-check-label" >Pending</label>
            </div>
            <button class="btn btn-lg btn-secondary w-100" type="submit"> Update Card </button><br />
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
        card_id:null,
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
    async updatecard(cardInfo){
      const response = await fetch("http://localhost:8080/api/card",{
            headers: {"Content-Type":"application/json","Authentication-Token":localStorage.getItem("token")},
            method: "put",
            body: JSON.stringify(cardInfo)
        }).catch(()=>this.error_message='Server is down')
      if(response){
        if(response.ok){
          this.$router.push({name:'dashboard'})
        }else{
        const e = await response.json()
        this.error_message=e.error_message
        }
      }
    }
  },
  async mounted() {document.title="Update Card"
  this.cardInfo.card_id=this.$route.params.card_id;
  if(this.cardInfo.card_id){
    const response = await fetch(`http://localhost:8080/api/card/${this.cardInfo.card_id}`,{
            headers: {"Content-Type":"application/json","Authentication-Token":localStorage.getItem("token")},
            method: "get"
        }).catch(()=>console.log('Server is down'))
      let d =  await response.json()
      this.cardInfo=d
      }
      else{
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