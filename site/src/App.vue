<script setup>
import axios from 'axios';

import MarathonsTable from './components/MarathonsTable.vue'
</script>

<template>
  <div>
    <header>
      <div class="wrapper">
        <div class="site-header">
          <h1>Marathon Records</h1>
          <p>Best and latest times from marathons worldwide.</p>
          <time class="last-updated" :datetime="lastUpdatedISO">
            Last updated: {{ lastUpdated }}
          </time>
        </div>
      </div>
    </header>
    
    <main>
      <div class="wrapper">
        <MarathonsTable 
          :marathons="marathons" 
          :bestTimes="bestTimes"
          :latestTimes="latestTimes" />
      </div>
    </main>
  </div>
</template>

<script>
export default {
  name: 'app',
  data() {
    const lastDeployTime = new Date('2025-09-09T08:40:10Z');
    return {
      marathons: [],
      bestTimes: [],
      latestTimes: [],
      lastUpdated: lastDeployTime.toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'long', 
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
      }),
      lastUpdatedISO: lastDeployTime.toISOString()
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

<style scoped>
.site-header {
  text-align: center;
  margin-bottom: 2rem;
  padding: 1.5rem;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border-radius: 10px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.site-header h1 {
  margin: 0 0 0.5rem 0;
  font-size: 2.5rem;
  font-weight: 700;
}

.site-header p {
  margin: 0 0 1rem 0;
  font-size: 1.1rem;
  opacity: 0.9;
  max-width: 600px;
  margin: 0 auto 1rem auto;
}

.last-updated {
  font-size: 0.9rem;
  opacity: 0.8;
  font-style: italic;
}

.wrapper {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem;
}
</style>
