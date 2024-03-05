<script setup>
defineProps({
  marathons: {
    type: Object,
    required: true
  }
})
</script>

<template>
  <div class="marathons-table">
    <b-list-group>
      <b-list-group-item v-for="marathon in marathons" :key="marathon.city"
        >{{ marathon.city }} - {{ marathon.date }}</b-list-group-item
      >
    </b-list-group>
  </div>
</template>


<style scoped>
.marathons-table {
    text-align: center;
}
</style>