<script setup>
import axios from 'axios';

import MarathonsTable from './components/MarathonsTable.vue'
</script>

<template>
  <div>
    <!-- Loading State -->
    <div v-if="isLoading" class="loading-container">
      <div class="loading-content">
        <div class="loading-spinner"></div>
        <h1>Marathon Records</h1>
      </div>
    </div>

    <!-- Main Content -->
    <div v-else>
      <main>
        <div class="wrapper">
          <MarathonsTable
            :marathons="marathons"
            :bestTimes="bestTimes"
            :latestTimes="latestTimes"
            :links="links" />
        </div>
      </main>

      <footer>
        <div class="wrapper">
          <time class="last-updated" :datetime="lastUpdatedISO">
            Last updated: {{ lastUpdated }}
          </time>
        </div>
      </footer>
    </div>
  </div>
</template>

<script>
export default {
  name: 'app',
  data() {
    return {
      marathons: [],
      bestTimes: [],
      latestTimes: [],
      links: {},
      lastUpdated: '',
      lastUpdatedISO: '',
      isLoading: true
    }
  },
  async created() {
    try {
      [
        { data: this.marathons },
        { data: this.bestTimes },
        { data: this.latestTimes },
        { data: this.links },
      ] = await axios.all([
        axios.get(`${import.meta.env.BASE_URL}marathons.json`),
        axios.get(`${import.meta.env.BASE_URL}best_times.json`),
        axios.get(`${import.meta.env.BASE_URL}latest_times.json`),
        axios.get(`${import.meta.env.BASE_URL}links.json`),
      ]);

      // Load last updated timestamp
      try {
        const response = await axios.get(`${import.meta.env.BASE_URL}last_update.txt`);
        const lastDeployTime = new Date(response.data.trim());
        this.lastUpdated = lastDeployTime.toLocaleDateString('en-US', {
          year: 'numeric',
          month: 'long',
          day: 'numeric',
          hour: '2-digit',
          minute: '2-digit'
        });
        this.lastUpdatedISO = lastDeployTime.toISOString();
      } catch (error) {
        console.warn('Could not load last update timestamp:', error);
      }
    } catch (error) {
      console.error('Failed to load marathon data:', error);
    } finally {
      this.isLoading = false;
    }
  },
}
</script>

<style scoped>
/* Loading styles */
.loading-container {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: var(--color-background);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.loading-content {
  text-align: center;
  color: var(--color-heading);
}

.loading-content h1 {
  font-size: 2.5rem;
  font-weight: 700;
  margin: 1rem 0 0.5rem 0;
}

.loading-content p {
  font-size: 1.1rem;
  opacity: 0.9;
  margin: 0;
}

.loading-spinner {
  width: 50px;
  height: 50px;
  border: 3px solid var(--color-border);
  border-top: 3px solid var(--color-heading);
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin: 0 auto 1rem auto;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

/* Site styles */

footer {
  margin-top: 1rem;
  padding: 1rem 0 0 0;
  text-align: center;
}

.last-updated {
  font-size: 0.9rem;
  opacity: 0.8;
  font-style: italic;
  color: var(--color-text);
}

.wrapper {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem;
}
</style>
