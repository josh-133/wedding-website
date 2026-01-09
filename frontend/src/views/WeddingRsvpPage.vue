<script setup>
import RsvpForm from '../components/rsvp/RsvpForm.vue'
</script>

<template>
  <div class="py-12 px-4">
    <div class="max-w-4xl mx-auto text-center mb-8">
      <router-link to="/" class="text-blue-400 hover:text-blue-500 text-sm mb-4 inline-block">
        &larr; Back to Home
      </router-link>
    </div>

    <RsvpForm
      event-slug="wedding"
      event-title="Wedding Celebration"
      event-date="Saturday, 22nd May 2027"
    />

    <div class="max-w-md mx-auto mt-8 text-center text-slate-400 text-sm">
      <p>Can't find your invite? Please contact us directly.</p>
    </div>
  </div>
</template>
