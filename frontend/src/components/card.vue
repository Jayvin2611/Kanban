<template>
<div class="card mt-2 shadow-lg" draggable="true" @dragstart="dragCard($event,card.id)">
    <div class="card-body p-2">
     <div class="card-title"><h3 class="font-weight-bold">{{card.title}}</h3></div><br>
     <div><p>{{card.content}} </p></div>
     <div>Deadline: {{date}}</div>
     <div>Current Status: {{card.completed ? "Complete" : "Pending"}}</div><br>
     <div class="btn-group">
     <router-link :to="{name:'updatecard',params:{card_id:card.id}}"><button class="btn btn-secondary btn-sm m-1">Update Card</button></router-link><br>
     <button class="btn btn-secondary btn-sm m-1" @click="deletecard(card.list_id,card.id)"> Delete card</button>
    </div>
</div>
</div>
</template>

<script>
export default {
    name: 'Card',
    props: [
        'card'
    ],
    methods:{
        deletecard(l_id,c_id){
            if(window.confirm("Do you want to delete this card ?")){
            fetch('http://localhost:8080/api/card',
        {
            headers: {"Content-Type":"application/json","Authentication-Token":localStorage.getItem('token')},
            method: "delete",
            body: JSON.stringify({id:c_id,list_id:l_id})
        }).then(r=> r.json()).then(d=>this.$parent.refreshList()).catch(e=>console.log(e))
        }
        },
        dragCard(event,card_id){
            console.log(card_id)
            event.dataTransfer.dropEffect = 'move',
            event.dataTransfer.effectAllowed = 'move',
            event.dataTransfer.setData('card_id',card_id)
        }
    },
    computed:{
        date(){
            const options = { year: 'numeric', month: '2-digit', day: '2-digit', hour: '2-digit', minute: '2-digit' };
            let date= new Date(this.card.deadline)
            return date.toLocaleString("en-in",options)
        }
    }
}

</script>


<style scoped>
</style>
