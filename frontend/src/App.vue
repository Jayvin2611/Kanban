<template>
  <div id="app">
    <NavBar></NavBar>
    <div class="scroll"><router-view/></div>
    
  </div>
</template>

<script>
import NavBar from "./components/navBar.vue";
export default {
  name: 'App',
  components:{
    NavBar
  }
}
</script>

<style>
.scroll {
    height: 100vh;
    overflow-y: auto
}
.scroll::-webkit-scrollbar {
  display: none;
}
</style>
