<script setup>
import axios from 'axios';

import MarathonsTable from './components/MarathonsTable.vue'
</script>

<template>
  <header>
    <div class="wrapper">
      <MarathonsTable 
        :marathons="marathons" 
        :bestTimes="bestTimes"
        :latestTimes="latestTimes" />
    </div>
  </header>
</template>

<script>
export default {
  name: 'app',
  data() {
    return {
      marathons: [],
      bestTimes: [],
      latestTimes: [],
    }
  },
  async created() {
    [
      { data: this.marathons }, 
      { data: this.bestTimes },
      { data: this.latestTimes },
    ] = await axios.all([
      axios.get('/marathons.json'), 
      axios.get('/best_times.json'),
      axios.get('/latest_times.json'),
    ]);
  },
}
</script>
