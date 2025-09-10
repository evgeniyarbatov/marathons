<script setup>
const props = defineProps({
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
  <section class="marathons-table" role="main" aria-label="Marathon records by city">
    <ul class="list-group" role="list">
      <li
        v-for="(marathon, index) in sortedMarathons"
        :key="marathon.city"
        class="list-group-item"
      >
        <header class="item-header">
          <h2>
            {{ marathon.City }}
            <div class="flag" role="img" :aria-label="`${marathon.City} country flag`">
              <span :class="`fi fi-${marathon.Country}`"></span>
            </div>
          </h2>
        </header>
        
        <div class="table-container">
          <table role="table" :aria-label="`Statistics for ${marathon.City} marathon`">
            <caption class="sr-only">Marathon statistics for {{ marathon.City }}</caption>
            <thead>
              <tr>
                <th scope="col">Countries</th>
                <th scope="col">Athletes</th>
                <th scope="col">Men</th>
                <th scope="col">Women</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="item in getCityInfo(marathon.City, marathons)" :key="item.id">
                <td>{{ item['Country Count'] }}</td>
                <td>{{ item['People Count'] }}</td>
                <td>{{ item.Men }}</td>
                <td>{{ item.Women }}</td>
              </tr>
            </tbody>
          </table>
        </div>
        
        <div class="times-section">
          <div class="times-row">
            <div class="times-col">
              <h3 class="section-heading">Best</h3>
              
              <div class="gender-section" v-if="getCityInfoByGender(marathon.City, bestTimes, 'Men').length > 0">
                <h4 class="gender-heading">Men</h4>
                <ul>
                  <li v-for="(bestTime, index) in getCityInfoByGender(marathon.City, bestTimes, 'Men')" :key="`best-men-${index}`">
                    {{ bestTime.Time }} - {{ bestTime.Name }}
                    <span :class="`fi fi-${bestTime.Country}`"></span>
                    ({{ bestTime.Year }})
                  </li>
                </ul>
              </div>

              <div class="gender-section" v-if="getCityInfoByGender(marathon.City, bestTimes, 'Women').length > 0">
                <h4 class="gender-heading">Women</h4>
                <ul>
                  <li v-for="(bestTime, index) in getCityInfoByGender(marathon.City, bestTimes, 'Women')" :key="`best-women-${index}`">
                    {{ bestTime.Time }} - {{ bestTime.Name }}
                    <span :class="`fi fi-${bestTime.Country}`"></span>
                    ({{ bestTime.Year }})
                  </li>
                </ul>
              </div>
            </div>

            <div class="times-col">
              <h3 class="section-heading">Latest</h3>
              
              <div class="gender-section" v-if="getCityInfoByGender(marathon.City, latestTimes, 'Men').length > 0">
                <h4 class="gender-heading">Men</h4>
                <ul>
                  <li v-for="(latestTime, index) in getCityInfoByGender(marathon.City, latestTimes, 'Men')" :key="`latest-men-${index}`">
                    {{ latestTime.Time }} - {{ latestTime.Name }}
                    <span :class="`fi fi-${latestTime.Country}`"></span>
                    ({{ latestTime.Year }})
                  </li>
                </ul>
              </div>

              <div class="gender-section" v-if="getCityInfoByGender(marathon.City, latestTimes, 'Women').length > 0">
                <h4 class="gender-heading">Women</h4>
                <ul>
                  <li v-for="(latestTime, index) in getCityInfoByGender(marathon.City, latestTimes, 'Women')" :key="`latest-women-${index}`">
                    {{ latestTime.Time }} - {{ latestTime.Name }}
                    <span :class="`fi fi-${latestTime.Country}`"></span>
                    ({{ latestTime.Year }})
                  </li>
                </ul>
              </div>
            </div>
          </div>
        </div>
      </li>
    </ul>
  </section>
</template>

<script>
export default {
  computed: {
    sortedMarathons() {
      return [...this.marathons].sort((a, b) => {
        const aBestTime = this.getBestTimeForCity(a.City);
        const bBestTime = this.getBestTimeForCity(b.City);
        
        if (!aBestTime && !bBestTime) return 0;
        if (!aBestTime) return 1;
        if (!bBestTime) return -1;
        
        return this.timeToSeconds(aBestTime) - this.timeToSeconds(bBestTime);
      });
    }
  },
  methods: {
    getCityInfo: function (city, info) {
      return info.filter(time => time.City === city)
    },
    getCityInfoByGender: function (city, info, gender) {
      return info.filter(time => time.City === city && time.Gender === gender)
    },
    getBestTimeForCity(city) {
      const menTimes = this.getCityInfoByGender(city, this.bestTimes, 'Men');
      const womenTimes = this.getCityInfoByGender(city, this.bestTimes, 'Women');
      const allTimes = [...menTimes, ...womenTimes];
      
      if (allTimes.length === 0) return null;
      
      return allTimes.reduce((best, current) => {
        const bestSeconds = this.timeToSeconds(best.Time);
        const currentSeconds = this.timeToSeconds(current.Time);
        return currentSeconds < bestSeconds ? current : best;
      }).Time;
    },
    timeToSeconds(timeString) {
      if (!timeString) return Infinity;
      const parts = timeString.split(':');
      if (parts.length === 3) {
        const hours = parseInt(parts[0], 10);
        const minutes = parseInt(parts[1], 10);
        const seconds = parseInt(parts[2], 10);
        return hours * 3600 + minutes * 60 + seconds;
      }
      return Infinity;
    }
  }
}
</script>

<style scoped>
.marathons-table {
  width: 100%;
  max-width: 800px;
  margin: auto;
}

.list-group {
  list-style: none;
  padding: 0;
  margin: 0;
}

.list-group-item {
  border: 1px solid #ccc;
  padding: 10px;
  margin-bottom: 10px;
  border-radius: 5px;
  background-color: #fff;
}

.list-group-item.disabled {
  opacity: 0.6;
  pointer-events: none;
}

.item-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 5px;
}

.item-header h2 {
  margin: 0;
  font-size: 1.25rem;
  font-weight: 600;
  color: #333;
  display: flex;
  align-items: center;
  gap: 10px;
}

.flag {
  display: inline-block;
  vertical-align: middle;
}

.table-container table {
  width: 100%;
  border-collapse: collapse;
}

.table-container th, .table-container td {
  text-align: center;
}

.times-section {
  margin-top: 15px;
}

.times-row {
  display: flex;
  justify-content: space-between;
  gap: 20px;
}

.times-col {
  flex: 1;
}

.gender-section {
  margin-bottom: 15px;
}

.gender-heading {
  margin: 0 0 8px 0;
  font-size: 0.75rem;
  font-weight: 500;
  color: #555;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

ul {
  padding: 0;
  list-style: none;
}

li {
  margin-bottom: 5px;
}

.section-heading {
  margin: 0 0 10px 0;
  font-size: 1rem;
  font-weight: 600;
  color: #333;
  border-bottom: 2px solid #667eea;
  padding-bottom: 5px;
}

.sr-only {
  position: absolute;
  width: 1px;
  height: 1px;
  padding: 0;
  margin: -1px;
  overflow: hidden;
  clip: rect(0, 0, 0, 0);
  white-space: nowrap;
  border: 0;
}
</style>
