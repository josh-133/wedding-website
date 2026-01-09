<script setup>
defineProps({
  rsvps: {
    type: Array,
    required: true
  }
})

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
            <th class="text-left px-4 py-3 text-sm font-medium text-slate-600">Name</th>
            <th class="text-left px-4 py-3 text-sm font-medium text-slate-600">Email</th>
            <th class="text-left px-4 py-3 text-sm font-medium text-slate-600">Event</th>
            <th class="text-center px-4 py-3 text-sm font-medium text-slate-600">Attending</th>
            <th class="text-left px-4 py-3 text-sm font-medium text-slate-600">Submitted</th>
          </tr>
        </thead>
        <tbody class="divide-y divide-slate-100">
          <tr v-if="rsvps.length === 0">
            <td colspan="5" class="px-4 py-8 text-center text-slate-400">
              No RSVPs yet
            </td>
          </tr>
          <tr v-for="rsvp in rsvps" :key="rsvp.id" class="hover:bg-slate-50">
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
        </tbody>
      </table>
    </div>
  </div>
</template>
