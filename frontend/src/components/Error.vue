<template>
    <div class="alert alert-warning alert-dismissible fade show text-center" role="alert">{{message}}
    <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
    </div>
</template>

<script>
export default {
  name: 'Error',
  props: [
    'message'
  ]
}
</script>

<style>
.alert {
    text-align: center;
}
</style>