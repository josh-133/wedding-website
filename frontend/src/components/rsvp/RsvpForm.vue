<script setup>
import { ref } from 'vue'
import { submitRsvp } from '../../api'

const props = defineProps({
  eventSlug: {
    type: String,
    required: true
  },
  eventTitle: {
    type: String,
    required: true
  },
  eventDate: {
    type: String,
    required: true
  }
})

const name = ref('')
const email = ref('')
const attending = ref(true)
const isSubmitting = ref(false)
const isSubmitted = ref(false)
const error = ref('')

async function handleSubmit() {
  if (!name.value.trim() || !email.value.trim()) {
    error.value = 'Please fill in all fields'
    return
  }

  isSubmitting.value = true
  error.value = ''

  try {
    await submitRsvp({
      event_slug: props.eventSlug,
      name: name.value.trim(),
      email: email.value.trim(),
      attending: attending.value
    })
    isSubmitted.value = true
  } catch (err) {
    error.value = err.response?.data?.detail || 'Something went wrong. Please try again.'
  } finally {
    isSubmitting.value = false
  }
}

function resetForm() {
  name.value = ''
  email.value = ''
  attending.value = true
  isSubmitted.value = false
  error.value = ''
}
</script>

<template>
  <div class="card max-w-md mx-auto">
    <!-- Success State -->
    <div v-if="isSubmitted" class="text-center py-8">
      <div class="w-16 h-16 bg-blue-100 rounded-full flex items-center justify-center mx-auto mb-4">
        <svg class="w-8 h-8 text-blue-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
        </svg>
      </div>
      <h3 class="font-serif text-2xl text-slate-800 mb-2">Thank You!</h3>
      <p class="text-slate-600 mb-6">
        Your RSVP for the {{ eventTitle }} has been received.
        <br />
        <span v-if="attending">We can't wait to see you!</span>
        <span v-else>We'll miss you!</span>
      </p>
      <button @click="resetForm" class="btn-secondary text-sm">
        Submit another RSVP
      </button>
    </div>

    <!-- Form -->
    <form v-else @submit.prevent="handleSubmit" class="space-y-6">
      <div class="text-center mb-8">
        <h2 class="font-serif text-3xl text-slate-800 mb-2">{{ eventTitle }}</h2>
        <p class="text-blue-500 font-medium">{{ eventDate }}</p>
      </div>

      <div>
        <label for="name" class="block text-slate-700 font-medium mb-2">Your Name</label>
        <input
          id="name"
          v-model="name"
          type="text"
          class="input-field"
          placeholder="Enter your full name"
          required
        />
      </div>

      <div>
        <label for="email" class="block text-slate-700 font-medium mb-2">Email Address</label>
        <input
          id="email"
          v-model="email"
          type="email"
          class="input-field"
          placeholder="your@email.com"
          required
        />
      </div>

      <div>
        <label class="block text-slate-700 font-medium mb-3">Will you be attending?</label>
        <div class="flex gap-4">
          <button
            type="button"
            @click="attending = true"
            :class="[
              'flex-1 py-3 px-4 rounded-lg border-2 transition-all font-medium',
              attending
                ? 'border-blue-300 bg-blue-50 text-blue-600'
                : 'border-slate-200 text-slate-500 hover:border-slate-300'
            ]"
          >
            Yes, I'll be there!
          </button>
          <button
            type="button"
            @click="attending = false"
            :class="[
              'flex-1 py-3 px-4 rounded-lg border-2 transition-all font-medium',
              !attending
                ? 'border-rose-200 bg-rose-50 text-rose-300'
                : 'border-slate-200 text-slate-500 hover:border-slate-300'
            ]"
          >
            Sorry, can't make it
          </button>
        </div>
      </div>

      <div v-if="error" class="p-4 bg-red-50 border border-red-200 rounded-lg text-red-600 text-sm">
        {{ error }}
      </div>

      <button
        type="submit"
        :disabled="isSubmitting"
        class="btn-primary w-full disabled:opacity-50 disabled:cursor-not-allowed"
      >
        <span v-if="isSubmitting">Submitting...</span>
        <span v-else>Submit RSVP</span>
      </button>
    </form>
  </div>
</template>
