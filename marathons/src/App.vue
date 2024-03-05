<script setup>
import PageHeader from './components/PageHeader.vue'
import MarathonsTable from './components/MarathonsTable.vue'
</script>

<template>
  <header>
    <div class="wrapper">
      <PageHeader text="World Marathons" />
      <MarathonsTable :marathons="marathons" />
    </div>
  </header>
</template>

<script>
export default {
  name: 'app',
  data() {
    return {
      marathons: [
        { city: 'Tokyo', date: '03/03' },
        { city: 'Boston', date: '15/04' },
        { city: 'London', date: '21/04' },
        { city: 'Berlin', date: '22/09' },
        { city: 'Chicago', date: '13/10' },
        { city: 'New York', date: '3/09' }
      ]
    }
  }
}
</script>
