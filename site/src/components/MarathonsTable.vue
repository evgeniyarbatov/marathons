<script setup>
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
    <ul class="list-group">
      <li
        v-for="(marathon, index) in marathons"
        :key="marathon.city"
        class="list-group-item"
      >
        <div class="item-header">
          <span>
            {{ marathon.City }}
            <div class="flag">
              <span :class="`fi fi-${marathon.Country}`"></span>
            </div>
          </span>
        </div>
        
        <div class="table-container">
          <table>
            <thead>
              <tr>
                <th>Countries</th>
                <th>Records</th>
                <th>Athletes</th>
                <th>Men</th>
                <th>Women</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="item in getCityInfo(marathon.City, marathons)" :key="item.id">
                <td>{{ item['Country Count'] }}</td>
                <td>{{ item['Record Count'] }}</td>
                <td>{{ item['People Count'] }}</td>
                <td>{{ item.Men }}</td>
                <td>{{ item.Women }}</td>
              </tr>
            </tbody>
          </table>
        </div>
        
        <div class="row">
          <div class="col">
            <h3 class="section-heading">Best</h3>
            <ul>
              <li v-for="(bestTime, index) in getCityInfo(marathon.City, bestTimes)" :key="index">
                {{ bestTime.Time }} - {{ bestTime.Name }}
                <span :class="`fi fi-${bestTime.Country}`"></span>
                ({{ bestTime.Year }})
              </li>
            </ul>
          </div>
          <div class="col">
            <h3 class="section-heading">Latest</h3>
            <ul>
              <li v-for="(latestTime, index) in getCityInfo(marathon.City, latestTimes)" :key="index">
                {{ latestTime.Time }} - {{ latestTime.Name }}
                <span :class="`fi fi-${latestTime.Country}`"></span>
                ({{ latestTime.Year }})
              </li>
            </ul>
          </div>
        </div>
      </li>
    </ul>
  </div>
</template>

<script>
export default {
  methods: {
    getCityInfo: function (city, info) {
      return info.filter(time => time.City === city)
    },
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

.row {
  display: flex;
  justify-content: space-between;
}

.col {
  width: 48%;
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
</style>
