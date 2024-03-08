<script setup>
import axios from 'axios';

import MarathonsTable from './components/MarathonsTable.vue'
</script>

<template>
  <header>
    <div class="wrapper">
      <MarathonsTable :marathons="marathons" :daysParsed="daysParsed" />
    </div>
  </header>
</template>

<script>
export default {
  name: 'app',
  data() {
    return {
      marathons: []
    }
  },
  created() {
    axios.get('/marathons.json')
      .then(response => {
        this.marathons = response.data;
      })
      .catch(error => {
        console.error('Error fetching data:', error);
      });
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
