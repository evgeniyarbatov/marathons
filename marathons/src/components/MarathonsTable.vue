<script setup>
  defineProps({
    marathons: {
      type: Object,
      required: true,
    },
    daysCounter: {
      type: Object,
      required: true,     
    },
  })
</script>

<template>
  <div class="marathons-table">
    <b-list-group>
      <b-list-group-item
        border-0
        v-for="(marathon, index) in marathons" :key="marathon.city"
      >
        {{ marathon.city }} - {{ daysCounter[index] }} @ {{ marathon.date }}
      </b-list-group-item
      >
    </b-list-group>
  </div>
</template>


<style scoped>
.marathons-table {
    text-align: center;
}
.list-group-item {
    padding: 30px 30px;
    border-style: none;
}
</style>