<template>
    <div class="container">
    <Error v-if="error_message" :message="error_message"></Error>
    <div class="row mt-5 d-flex justify-content-center align-items-center vh-75">
      <div class="col-12 col-md-8 col-lg-6 col-xl-5">
        <div class="card border-0 shadow">
          <div class="card-body">
            <p>
                <h3> Name  : {{ user.first_name }}</h3>
                <h3> Last Name     : {{ user.last_name }}</h3>
                <h3> Email Address : {{ user.email }} </h3>
            </p>
            <router-link to="/chat"><button  class="btn btn-lg btn-secondary w-100">Add/Update Chat link</button></router-link>
          </div>
        </div>
        </div>
    </div>
    </div>
</template>


<script>
export default {
    data(){
        return {
            user:{
            first_name:null,
            last_name:null,
            email:null,
            error_message:null
        }}
    },
    mounted(){
        document.title="User Info"
        fetch('http://localhost:8080/api/user',
        {
            headers: {"Content-Type":"application/json","Authentication-Token":localStorage.getItem("token")},
            method: "get"
        }).then(r=> r.json()).then(d=>this.user=d).catch(e=>this.error_message='Opps Something went wrong')
    }
}
</script>