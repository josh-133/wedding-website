<script setup>
import { ref } from 'vue'

defineProps({
  rsvps: {
    type: Array,
    required: true
  }
})

const expandedRows = ref(new Set())

function toggleRow(id) {
  if (expandedRows.value.has(id)) {
    expandedRows.value.delete(id)
  } else {
    expandedRows.value.add(id)
  }
}

function isExpanded(id) {
  return expandedRows.value.has(id)
}

function formatDate(dateStr) {
  const date = new Date(dateStr)
  return date.toLocaleDateString('en-AU', {
    day: 'numeric',
    month: 'short',
    year: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}
</script>

<template>
  <div class="bg-white rounded-xl shadow-sm border border-slate-200 overflow-hidden">
    <div class="overflow-x-auto">
      <table class="w-full">
        <thead class="bg-slate-50 border-b border-slate-200">
          <tr>
            <th class="text-left px-4 py-3 text-sm font-medium text-slate-600 w-8"></th>
            <th class="text-left px-4 py-3 text-sm font-medium text-slate-600">Name</th>
            <th class="text-left px-4 py-3 text-sm font-medium text-slate-600">Email</th>
            <th class="text-left px-4 py-3 text-sm font-medium text-slate-600">Event</th>
            <th class="text-center px-4 py-3 text-sm font-medium text-slate-600">Guests</th>
            <th class="text-center px-4 py-3 text-sm font-medium text-slate-600">Attending</th>
            <th class="text-left px-4 py-3 text-sm font-medium text-slate-600">Submitted</th>
          </tr>
        </thead>
        <tbody class="divide-y divide-slate-100">
          <tr v-if="rsvps.length === 0">
            <td colspan="7" class="px-4 py-8 text-center text-slate-400">
              No RSVPs yet
            </td>
          </tr>
          <template v-for="rsvp in rsvps" :key="rsvp.id">
            <tr
              class="hover:bg-slate-50 cursor-pointer"
              @click="toggleRow(rsvp.id)"
            >
              <td class="px-4 py-3">
                <button
                  class="text-slate-400 hover:text-slate-600 transition-transform"
                  :class="{ 'rotate-90': isExpanded(rsvp.id) }"
                >
                  <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
                  </svg>
                </button>
              </td>
              <td class="px-4 py-3 text-slate-800">{{ rsvp.name }}</td>
              <td class="px-4 py-3 text-slate-600 text-sm">{{ rsvp.email }}</td>
              <td class="px-4 py-3">
                <span
                  :class="[
                    'px-2 py-1 rounded-full text-xs font-medium',
                    rsvp.event_slug === 'engagement'
                      ? 'bg-blue-100 text-blue-600'
                      : 'bg-slate-100 text-slate-600'
                  ]"
                >
                  {{ rsvp.event_name }}
                </span>
              </td>
              <td class="px-4 py-3 text-center">
                <span class="text-slate-700 font-medium">{{ rsvp.guest_count }}</span>
              </td>
              <td class="px-4 py-3 text-center">
                <span
                  :class="[
                    'inline-flex items-center justify-center w-6 h-6 rounded-full text-xs font-bold',
                    rsvp.attending
                      ? 'bg-green-100 text-green-600'
                      : 'bg-rose-100 text-rose-500'
                  ]"
                >
                  {{ rsvp.attending ? '✓' : '✗' }}
                </span>
              </td>
              <td class="px-4 py-3 text-slate-500 text-sm">{{ formatDate(rsvp.submitted_at) }}</td>
            </tr>
            <!-- Expanded Guest Details -->
            <tr v-if="isExpanded(rsvp.id) && rsvp.guests && rsvp.guests.length > 0">
              <td colspan="7" class="bg-slate-50 px-4 py-3">
                <div class="ml-8">
                  <p class="text-sm font-medium text-slate-600 mb-2">Guest Details:</p>
                  <div class="grid gap-2">
                    <div
                      v-for="guest in rsvp.guests"
                      :key="guest.id"
                      class="flex items-center gap-4 text-sm"
                    >
                      <span
                        :class="[
                          'px-2 py-0.5 rounded text-xs',
                          guest.is_primary
                            ? 'bg-blue-100 text-blue-600'
                            : 'bg-slate-200 text-slate-600'
                        ]"
                      >
                        {{ guest.is_primary ? 'Primary' : 'Guest' }}
                      </span>
                      <span class="text-slate-800">{{ guest.name }}</span>
                      <span v-if="guest.dietary_requirements" class="text-slate-500">
                        Dietary: {{ guest.dietary_requirements }}
                      </span>
                    </div>
                  </div>
                </div>
              </td>
            </tr>
          </template>
        </tbody>
      </table>
    </div>
  </div>
</template>
