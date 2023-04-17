<template>
    <div class="col-sm-5 col-md-4 col-xl-3 col-8">
      <div class="card bg-light" style="height:max-content;min-height:100vh;">
      <div class="card-body" @drop="cardDrop($event,list.id)" @dragenter.prevent @dragover.prevent>
        <div class="card-title">
            <h3 class="font-weight-bold">{{ list.name }}</h3>
        </div>
        <div class="btn-group">
        <router-link :to="{name:'updatelist',params:{list_id:list.id}}"><button class="btn btn-secondary btn-sm m-1">Update List</button></router-link><br>
        <button class="btn btn-secondary btn-sm m-1" @click="deletelist(list.id)"> Delete List</button>
        <router-link :to="{name:'addcard',params:{list_id:list.id}}"><button class="btn btn-secondary btn-sm m-1" >Add Card</button></router-link>
        <button @click="download(list.id)" class="btn btn-secondary btn-sm m-1"> Download All Card</button>
      </div>
        <div v-if="list.cards.length!=0" class="items p-2">
        <Card :key="card.id" v-for="card in list.cards" :card="card"/>
      </div>
      </div>
    </div>
    </div>
</template>

<script>
import Card from './card.vue';
export default {
  name: 'List',
  components: { Card
        },
  props: [
    'list'
  ],
  methods:{
    refreshList(){
      fetch(`http://localhost:8080/api/list/${this.list.id}`,
        {
            headers: {"Content-Type":"application/json","Authentication-Token":localStorage.getItem('token')},
            method: "get"
        }).then(r=> r.json()).then(d=>this.list=d).catch(e=>console.log(e))
    },
    deletelist(l_id){
          if(window.confirm("Do you want to delete this List?")){
          fetch('http://localhost:8080/api/list',
      {
          headers: {"Content-Type":"application/json","Authentication-Token":localStorage.getItem('token')},
          method: "delete",
          body: JSON.stringify({id:l_id})
      }).then(r=> r.json()).then(d=>this.$parent.refresh()).catch(e=>console.log(e))
      }},
      async download(id){
            var a = await fetch(`http://localhost:8080/api/export/${id}` ,
            {headers: {"Content-Type":"application/json","Authentication-Token":localStorage.getItem('token')}}
            ).catch(e=>console.log(e))
            var b = await a.blob()
            var url = window.URL.createObjectURL(b)
            var d = document.createElement("a")
            d.href = url
            d.setAttribute("download",`${this.list.name}.csv`)
            document.body.appendChild(d)
            d.click()
            d.remove()
        },
        async cardDrop(event,list_id){
          let card_id = event.dataTransfer.getData('card_id')
          const response = await fetch("http://localhost:8080/api/dragdrop",{
            headers: {"Content-Type":"application/json","Authentication-Token":localStorage.getItem("token")},
            method: "put",
            body: JSON.stringify({card_id:card_id,list_id:list_id})
            }).catch(()=>console.log('Server is down'))
            if(response){
              if(response.ok){
                this.$parent.refresh()
                console.log('Transfered')
              }else{
              const e = await response.json()
              console.log(e.error_message)
              }
            }
        }
  }
}
</script>

<style scoped>
/* .card {
  height: 100vh;
} */
</style>