<script setup>
import axios from 'axios';

import MarathonsTable from './components/MarathonsTable.vue'
</script>

<template>
  <header>
    <div class="wrapper">
      <MarathonsTable 
        :marathons="marathons" 
        :summaryInfo="summaryInfo"
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
      summaryInfo: [],
    }
  },
  async created() {
    [
      { data: this.marathons }, 
      { data: this.bestTimes },
      { data: this.latestTimes },
      { data: this.summaryInfo },
    ] = await axios.all([
      axios.get('/marathons.json'), 
      axios.get('/best_times.json'),
      axios.get('/latest_times.json'),
      axios.get('/marathon_summary.json'),
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
        return self.parseDate(marathon.date)
      })
    }
  }
}
</script>
