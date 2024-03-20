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
  latestTimes: {
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
              {{ formatDate(daysParsed[index]) }}
            </div>
          {{ marathon.City }}
          <div class="flag">
            <country-flag :country="marathon.Country" size="normal" />
          </div>
          <small>{{ getDaysMessage(daysParsed[index]) }}</small>
        </div>
        <p class="mb-1">
          <b-table 
            class="text-center"
            :items="getCityInfo(marathon.City, marathons)"
            :fields="[
              { key: 'Country Count', label: 'Countries' },
              { key: 'Record Count', label: 'Records' },
              { key: 'People Count', label: 'Athletes' },
              { key: 'Men', label: 'Men' },
              { key: 'Women', label: 'Women' },
            ]"
          >
          </b-table>
        </p>
        <b-container fluid>
          <b-row>
            <b-col>
              <p class="mb-1">
                <ul>
                  <li
                    v-for="(bestTime, index) in getCityInfo(marathon.City, bestTimes)"
                    :key="index"
                  >
                    {{ bestTime.Time }} - 
                    {{ bestTime.Name }}
                    <country-flag :country="bestTime.Country" size="small" />
                    ({{ bestTime.Year }})
                  </li>
                </ul>
              </p>
            </b-col>
            <b-col>
              <p class="mb-1">
                <ul>
                  <li
                    v-for="(latestTime, index) in getCityInfo(marathon.City, latestTimes)"
                    :key="index"
                  >
                    {{ latestTime.Time }} - 
                    {{ latestTime.Name }}
                    <country-flag :country="latestTime.Country" size="small" />
                    ({{ latestTime.Year }})
                  </li>
                </ul>
              </p>
            </b-col>
          </b-row>
      </b-container>
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
    getCityInfo: function (city, info) {
      return info.filter(time => time.City === city)
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
