<script setup>
import MarathonsTable from './components/MarathonsTable.vue'
</script>

<template>
  <header>
    <div class="wrapper">
      <MarathonsTable 
        :marathons="marathons"
        :daysParsed="daysParsed"
      />
    </div>
  </header>
</template>

<script>
export default {
  name: 'app',
  data() {
    return {
      marathons: [
        { city: 'Tokyo', country: 'jp', date: '3/3' },
        { city: 'Boston', country: 'us', date: '15/4' },
        { city: 'London', country: 'gb', date: '21/4' },
        { city: 'Berlin', country: 'de', date: '22/9' },
        { city: 'Chicago', country: 'us', date: '13/10' },
        { city: 'New York', country: 'us', date: '3/9' }
      ]
    }
  },
  methods: {
    parseDate(date) {
      const parts = date.split('/');
      const year = (new Date()).getFullYear();
      const month = parseInt(parts[1]) - 1;
      const day = parseInt(parts[0]); 
      return new Date(year, month, day);
    },
  },
  computed: {
    daysParsed: function() {
      const self = this;
        return this.marathons.map(function(marathon) {
          return self.parseDate(marathon.date);
        });
    },
  }
}
</script>
