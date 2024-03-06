<script setup>
import PageHeader from './components/PageHeader.vue'
import MarathonsTable from './components/MarathonsTable.vue'
</script>

<template>
  <header>
    <div class="wrapper">
      <PageHeader text="World Marathon Majors" />
      <MarathonsTable 
        :marathons="marathons"
        :daysCounter="daysCounter"
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
        { city: 'Tokyo', date: '3/3' },
        { city: 'Boston', date: '15/4' },
        { city: 'London', date: '21/4' },
        { city: 'Berlin', date: '22/9' },
        { city: 'Chicago', date: '13/10' },
        { city: 'New York', date: '3/9' }
      ]
    }
  },
  computed: {
    daysCounter: function() {
        return this.marathons.map(function(marathon) {
          const parts = marathon.date.split('/');

          const year = (new Date()).getFullYear();
          const month = parseInt(parts[1]) - 1; // Months are zero-based in JavaScript
          const day = parseInt(parts[0]);

          const difference = new Date() - new Date(year, month, day);
          const daysDifference = Math.floor(difference / (1000 * 60 * 60 * 24));

          if (daysDifference > 0) {
              return daysDifference + ' days ago';
          } else if (daysDifference < 0) {
              return Math.abs(daysDifference) + ' days until';
          } else {
              return 'Today';
          }
        });
    }
  }
}
</script>
