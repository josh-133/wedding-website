<script setup>
import { ref, onMounted, watch } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import { getAdminRsvps, getAdminStats, exportRsvps } from '../api'
import StatsCards from '../components/admin/StatsCards.vue'
import RsvpTable from '../components/admin/RsvpTable.vue'

const router = useRouter()
const authStore = useAuthStore()

const stats = ref([])
const rsvps = ref([])
const loading = ref(true)
const selectedEvent = ref('')
const exportLoading = ref(false)

async function loadData() {
  loading.value = true
  try {
    const [statsRes, rsvpsRes] = await Promise.all([
      getAdminStats(),
      getAdminRsvps(selectedEvent.value || null)
    ])
    stats.value = statsRes.data
    rsvps.value = rsvpsRes.data
  } catch (err) {
    if (err.response?.status === 401) {
      authStore.logout()
      router.push('/admin')
    }
    console.error('Failed to load data:', err)
  } finally {
    loading.value = false
  }
}

async function handleExport() {
  exportLoading.value = true
  try {
    const response = await exportRsvps(selectedEvent.value || null)
    const blob = new Blob([response.data], { type: 'text/csv' })
    const url = window.URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = selectedEvent.value ? `rsvps_${selectedEvent.value}.csv` : 'rsvps_all.csv'
    document.body.appendChild(a)
    a.click()
    document.body.removeChild(a)
    window.URL.revokeObjectURL(url)
  } catch (err) {
    console.error('Export failed:', err)
  } finally {
    exportLoading.value = false
  }
}

watch(selectedEvent, () => {
  loadData()
})

onMounted(() => {
  loadData()
})
</script>

<template>
  <div class="py-8 px-4">
    <div class="max-w-6xl mx-auto">
      <!-- Header -->
      <div class="flex flex-col md:flex-row md:items-center md:justify-between mb-8 gap-4">
        <div>
          <h1 class="font-serif text-3xl text-slate-800">RSVP Dashboard</h1>
          <p class="text-slate-500">Manage and view all responses</p>
        </div>
        <button
          @click="handleExport"
          :disabled="exportLoading"
          class="btn-secondary flex items-center gap-2 self-start"
        >
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
              d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
          </svg>
          <span v-if="exportLoading">Exporting...</span>
          <span v-else>Export CSV</span>
        </button>
      </div>

      <!-- Loading -->
      <div v-if="loading" class="py-12 text-center">
        <div class="animate-pulse text-blue-400">Loading dashboard...</div>
      </div>

      <template v-else>
        <!-- Stats -->
        <StatsCards :stats="stats" />

        <!-- Filter -->
        <div class="mb-6 flex items-center gap-4">
          <label class="text-slate-600 text-sm">Filter by event:</label>
          <select
            v-model="selectedEvent"
            class="input-field w-auto"
          >
            <option value="">All Events</option>
            <option value="engagement">Engagement Party</option>
            <option value="wedding">Wedding</option>
          </select>
        </div>

        <!-- Table -->
        <RsvpTable :rsvps="rsvps" />
      </template>
    </div>
  </div>
</template>
