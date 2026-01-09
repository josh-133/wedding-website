<script setup>
import { ref, onMounted } from 'vue'
import { getEvents } from '../api'

const events = ref([])
const loading = ref(true)

const eventDetails = {
  engagement: {
    title: 'Engagement Party',
    description: 'Join us to celebrate the beginning of our journey together.',
    icon: '💍'
  },
  wedding: {
    title: 'Wedding Day',
    description: 'We invite you to witness our love as we say "I do".',
    icon: '💒'
  }
}

function formatDate(dateStr) {
  const date = new Date(dateStr)
  return date.toLocaleDateString('en-AU', {
    weekday: 'long',
    day: 'numeric',
    month: 'long',
    year: 'numeric'
  })
}

onMounted(async () => {
  try {
    const response = await getEvents()
    events.value = response.data
  } catch (err) {
    console.error('Failed to load events:', err)
  } finally {
    loading.value = false
  }
})
</script>

<template>
  <div class="py-12 px-4">
    <!-- Hero Section -->
    <section class="max-w-4xl mx-auto text-center mb-16">
      <p class="text-blue-400 uppercase tracking-widest text-sm mb-4">You're Invited</p>
      <h1 class="font-serif text-5xl md:text-6xl text-slate-800 mb-4">
        Isabella & Joshua
      </h1>
      <p class="text-xl text-slate-600 max-w-2xl mx-auto">
        We're so excited to share our special moments with you.
        Please let us know if you can join us!
      </p>
    </section>

    <!-- Decorative Divider -->
    <div class="flex items-center justify-center gap-4 mb-16">
      <div class="h-px bg-blue-200 w-24"></div>
      <span class="text-blue-300 text-2xl">✦</span>
      <div class="h-px bg-blue-200 w-24"></div>
    </div>

    <!-- Events Section -->
    <section class="max-w-4xl mx-auto">
      <div v-if="loading" class="text-center py-12">
        <div class="animate-pulse text-blue-400">Loading events...</div>
      </div>

      <div v-else class="grid md:grid-cols-2 gap-8">
        <router-link
          v-for="event in events"
          :key="event.id"
          :to="`/${event.slug}`"
          class="card hover:shadow-lg transition-all duration-300 hover:-translate-y-1 group"
        >
          <div class="text-center">
            <span class="text-4xl mb-4 block">
              {{ eventDetails[event.slug]?.icon || '📅' }}
            </span>
            <h2 class="font-serif text-2xl text-slate-800 mb-2 group-hover:text-blue-500 transition-colors">
              {{ eventDetails[event.slug]?.title || event.name }}
            </h2>
            <p class="text-blue-500 font-medium mb-4">
              {{ formatDate(event.event_date) }}
            </p>
            <p class="text-slate-600 mb-6">
              {{ eventDetails[event.slug]?.description || event.description }}
            </p>
            <span class="btn-secondary inline-block">
              RSVP Now
            </span>
          </div>
        </router-link>
      </div>
    </section>

    <!-- Registry Link -->
    <section class="max-w-4xl mx-auto text-center mt-16">
      <div class="h-px bg-slate-200 w-48 mx-auto mb-8"></div>
      <p class="text-slate-600 mb-4">Looking for our gift registry?</p>
      <router-link to="/registry" class="text-blue-500 hover:text-blue-600 font-medium underline">
        View Registry
      </router-link>
    </section>
  </div>
</template>
