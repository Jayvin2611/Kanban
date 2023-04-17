<template>
    <div class="container">    
    <div class="row mt-5 d-flex justify-content-center align-items-center vh-75">
      <div class="col-12 col-md-8 col-lg-6 col-xl-5">
        <div class="card border-0">
          <div class="card-body text-center">
           <apexchart type="pie"  :options="options" :series="summary.series"></apexchart>
           <h3 style="margin-top:20px;">This Months Summary</h3>
          </div>
        </div>
        </div>
      </div>
        
        <table>
          <thead>
            <tr>
            <th scope="col">Name</th>
            <th scope="col">Number</th>
        </tr>
        </thead>
        <tbody>
          <tr>
          <td> No of Total Card Created </td>
          <td>{{ this.summary.total }}</td>
        </tr>
        <tr>
          <td> No of Completed Card</td>
          <td>{{ this.summary.completed }}</td>
        </tr>
        <tr>
          <td> No of Pending Card</td>
          <td>{{ this.summary.pending }}</td>
        </tr>
        <tr>
          <td> No of Overdue Card</td>
          <td>{{ this.summary.overdue }}</td>
        </tr>
        </tbody>
        </table>
    </div>
</template>


<script>
import apexchart from 'vue-apexcharts';

export default {
    data(){
      return {
      summary:{
        total : null,
        completed: null,
        pending : null,
        overdue : null,
        series : null
      },
      options: {labels: ['No of completed cards', 'No of pending cards']}
    }},
    components:{
      apexchart : apexchart
    },    
    mounted() {
        document.title="Summary"
        fetch("http://localhost:8080/api/chart",
        {
            headers: {"Content-Type":"application/json","Authentication-Token":localStorage.getItem("token")},
            method: "get"
        }).then(r=> r.json()).then(d=>this.summary=d).catch(e=>console.log(e))
    }
  }
</script>

<style scoped>
table,th,td{
  margin: auto;
  border: 1px solid; 
  text-align: center;
}
</style>