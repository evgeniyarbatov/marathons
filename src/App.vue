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
        :latestTimes="latestTimes"
        :daysParsed="daysParsed" />
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
      axios.get(
        process.env.NODE_ENV === 'development'
        ? '/marathons.json'  
        : '/marathons/marathons.json'
      ), 
      axios.get(
        process.env.NODE_ENV === 'development'
        ? '/best_times.json'  
        : '/marathons/best_times.json'
      ),
      axios.get(
        process.env.NODE_ENV === 'development'
        ? '/latest_times.json'  
        : '/marathons/latest_times.json'   
      ),
    ]);
  },
  methods: {
    parseDate(date) {
      const parts = date.split('/')
      const year = new Date().getFullYear()
      const month = parseInt(parts[1]) - 1
      const day = parseInt(parts[0])
      return new Date(year, month, day)
    }
  },
  computed: {
    daysParsed: function () {
      const self = this
      return this.marathons.map(function (marathon) {
        return self.parseDate(marathon.Date)
      })
    }
  }
}
</script>
