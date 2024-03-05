<script setup>
defineProps({
  text: {
    type: String,
    required: true
  }
})
</script>

<template>
  <div class="header-text">
    <h1>{{ text }}</h1>
    <h3>Information about upcoming marathons</h3>
  </div>
</template>

<style scoped>
h1 {
  font-weight: 500;
  font-size: 2.6rem;
  position: relative;
  top: -10px;
}
h3 {
  font-size: 1.2rem;
}
.header-text h1,
.header-text h3 {
  text-align: center;
}
@media (min-width: 1024px) {
  .header-text h1,
  .header-text h3 {
    text-align: left;
  }
}
</style>
