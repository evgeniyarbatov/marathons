<script setup>
  defineProps({
    marathons: {
      type: Object,
      required: true,
    },
    daysParsed: {
      type: Object,
      required: true,     
    },
  })
</script>

<template>
  <div class="marathons-table">
    <b-list-group>
      <b-list-group-item
        v-for="(marathon, index) in marathons" :key="marathon.city"
        :disabled="isDateInPast(daysParsed[index])"
      >
        {{ marathon.city }} - 
        {{ this.getDaysMessage(daysParsed[index]) }} 
        {{ this.formatDate(daysParsed[index]) }}
      </b-list-group-item
      >
    </b-list-group>
  </div>
</template>

<script>
export default {
  methods: {
    isDateInPast(date) {
      return date < new Date();
    },
    formatDate(date) {
      return date.toLocaleDateString('en-US', {
        month: 'long', 
        day: 'numeric' 
      });
    },
    getDaysMessage: function(date) {
      const difference = new Date() - date;
      const daysDifference = Math.floor(difference / (1000 * 60 * 60 * 24));
      if (daysDifference > 0) {
          return daysDifference + ' days ago on';
      } else if (daysDifference < 0) {
          return Math.abs(daysDifference) + ' days until';
      } else {
          return 'today on';
      }
    },
  }
};
</script>

<style scoped>
.marathons-table {
    text-align: center;
    font-size: 3vw;
}
.list-group-item {
    padding: 30px 30px;
    border-style: none;
}
</style>