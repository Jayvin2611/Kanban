<template>
    <div>
        <nav class="navbar navbar-dark bg-dark">
            <router-link to="/"><a class="navbar-brand m-2"><img src="../assets/logo.png" alt="logo" height="45"></a></router-link>
            <router-link v-if="routename" to="/signup"><button class="btn btn-light me-2">Signup</button></router-link>
            <div  v-else>
            <router-link to="/user"><button class="btn btn-light me-2">User Info</button></router-link>
            <router-link to="/summary"><button class="btn btn-light me-2">Summary</button></router-link>
            <button class="btn btn-light me-2" @click="logout">Logout</button>
          </div>
        </nav>
    </div>
</template>

<script>
export default {
  name: 'NavBar',
  computed:{
    routename(){
        return this.$route.name==='home' || this.$route.name==='sign-up' ;
    }
  },
  methods:{
    logout(){
        localStorage.removeItem('token');
        this.$router.push({name:'home'})
    }
  }
}
</script>