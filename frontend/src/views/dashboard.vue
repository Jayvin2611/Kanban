<template>
    <div class="text text-center p-3">
  <Error v-if="error_message" :message="error_message"></Error>
        <div class="col-sm-6 col-md-4 col-xl-3">
            <router-link :to="{name:'addlist'}"><button class="btn btn-secondary btn-lg m-1">Add List</button></router-link>
        </div>
        <div class="row flex-row flex-sm-nowrap py-3">
        <List :key="list.id" v-for="list in lists" :list="list"/>
        </div>
    </div>
</template>

<script>
import { RouterLink } from "vue-router";
import List from "../components/list.vue";
import Error from "../components/Error.vue"

export default {
    data(){
        return{
                lists:null,
                error_message:null
            }
        },    
    mounted() {
            document.title="Dashboard"
            this.refresh()
        },
    components:{
        List,
        RouterLink,
        Error
        },
    methods:{
        async refresh(){
            this.error_message=null
            const response = await fetch("http://localhost:8080/api/list",{
            headers: {"Content-Type":"application/json","Authentication-Token":localStorage.getItem("token")},
            method: "get"
        }).catch(()=>this.error_message='Server is down')

        if(response){
        if(response.ok){
          const d = await response.json()
          this.lists=d
        }else{
          const e = await response.json()
          this.error_message=e.error_message
        }
      }
    }
    }
}
</script>



<style>

</style>