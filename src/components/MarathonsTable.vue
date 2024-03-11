<script setup>
import CountryFlag from 'vue-country-flag'

defineProps({
  marathons: {
    type: Object,
    required: true
  },
  bestTimes: {
    type: Object,
    required: true
  },
  daysParsed: {
    type: Object,
    required: true
  }
})
</script>

<template>
  <div class="marathons-table">
    <b-list-group>
      <b-list-group-item
        v-for="(marathon, index) in marathons"
        :key="marathon.city"
        :disabled="isDateInPast(daysParsed[index])"
        class="flex-column align-items-start"
      >
        <div class="d-flex w-100 justify-content-between align-items-center">
          <div class="marathon-date">
              {{ this.formatDate(daysParsed[index]) }}
            </div>
          {{ marathon.city }}
          <div class="flag">
            <country-flag :country="marathon.country" size="normal" />
          </div>
          <small>{{ this.getDaysMessage(daysParsed[index]) }}</small>
        </div>
        <p class="mb-1">
          <ul>
            <li
              v-for="(bestTime, index) in this.getBestRunningTime(marathon.city)"
              :key="index"
            >
              {{ bestTime.Time }} - 
              {{ bestTime.Name }}
              <country-flag :country="bestTime.Country" size="small" />
              -
              {{ bestTime.Date }}
            </li>
          </ul>
        </p>
      </b-list-group-item>
    </b-list-group>
  </div>
</template>

<script>
export default {
  methods: {
    isDateInPast(date) {
      return date < new Date()
    },
    formatDate(date) {
      return date.toLocaleDateString('en-US', {
        month: 'long',
        day: 'numeric'
      })
    },
    getDaysMessage: function (date) {
      const difference = new Date() - date
      const daysDifference = Math.floor(difference / (1000 * 60 * 60 * 24))
      if (daysDifference > 0) {
        return daysDifference + ' days ago'
      } else if (daysDifference < 0) {
        return Math.abs(daysDifference) + ' days to go'
      } else {
        return 'today on'
      }
    },
    getBestRunningTime: function (city) {
      return this.bestTimes.filter(time => time.City === city)
    },
  }
}
</script>

<style scoped>
.list-group-item {
  border-style: none;
}
.flag {
  display: inline-block;
  vertical-align: middle;
}
ul {
  list-style-type: none;
  padding: 0;
}
</style>
