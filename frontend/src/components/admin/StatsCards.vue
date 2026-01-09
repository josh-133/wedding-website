<script setup>
defineProps({
  stats: {
    type: Array,
    required: true
  }
})
</script>

<template>
  <div class="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8">
    <template v-for="stat in stats" :key="stat.event_slug">
      <div class="bg-white rounded-xl p-4 shadow-sm border border-slate-200">
        <p class="text-slate-500 text-sm mb-1">{{ stat.event_name }}</p>
        <p class="text-2xl font-bold text-slate-800">{{ stat.total_responses }}</p>
        <p class="text-xs text-slate-400">responses</p>
      </div>
      <div class="bg-blue-50 rounded-xl p-4 shadow-sm border border-blue-100">
        <p class="text-blue-500 text-sm mb-1">{{ stat.event_name }} Attending</p>
        <p class="text-2xl font-bold text-blue-600">{{ stat.attending }}</p>
        <p class="text-xs text-blue-400">confirmed</p>
      </div>
    </template>
  </div>
</template>
