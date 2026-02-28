<script setup>
import { ref, computed } from 'vue'
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

const MAX_GUESTS = 5

// Primary contact fields
const name = ref('')
const email = ref('')
const postalAddress = ref('')
const dietaryRequirements = ref('')
const attending = ref(true)

// Additional guests (up to 4 more, since primary counts as 1)
const additionalGuests = ref([])

const isSubmitting = ref(false)
const isSubmitted = ref(false)
const error = ref('')

const totalGuestCount = computed(() => 1 + additionalGuests.value.length)
const canAddMoreGuests = computed(() => totalGuestCount.value < MAX_GUESTS)

function addGuest() {
  if (canAddMoreGuests.value) {
    additionalGuests.value.push({ name: '', dietaryRequirements: '' })
  }
}

function removeGuest(index) {
  additionalGuests.value.splice(index, 1)
}

async function handleSubmit() {
  if (!name.value.trim() || !email.value.trim()) {
    error.value = 'Please fill in your name and email'
    return
  }

  // Validate additional guest names
  for (let i = 0; i < additionalGuests.value.length; i++) {
    if (!additionalGuests.value[i].name.trim()) {
      error.value = `Please enter a name for guest ${i + 2}`
      return
    }
  }

  isSubmitting.value = true
  error.value = ''

  try {
    // Build guests array (additional guests only - primary is sent separately)
    const guests = additionalGuests.value.map(g => ({
      name: g.name.trim(),
      dietary_requirements: g.dietaryRequirements.trim() || null
    }))

    await submitRsvp({
      event_slug: props.eventSlug,
      name: name.value.trim(),
      email: email.value.trim(),
      postal_address: postalAddress.value.trim() || null,
      attending: attending.value,
      dietary_requirements: dietaryRequirements.value.trim() || null,
      guests: guests
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
  postalAddress.value = ''
  dietaryRequirements.value = ''
  attending.value = true
  additionalGuests.value = []
  isSubmitted.value = false
  error.value = ''
}
</script>

<template>
  <div class="card max-w-lg mx-auto">
    <!-- Success State -->
    <div v-if="isSubmitted" class="text-center py-8">
      <div class="w-16 h-16 bg-blue-100 rounded-full flex items-center justify-center mx-auto mb-4">
        <svg class="w-8 h-8 text-blue-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
        </svg>
      </div>
      <h3 class="font-serif text-2xl text-slate-800 mb-2">Thank You!</h3>
      <p class="text-slate-600 mb-6">
        Your RSVP for {{ totalGuestCount }} {{ totalGuestCount === 1 ? 'guest' : 'guests' }} to the {{ eventTitle }} has been received.
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

      <!-- Attending Toggle -->
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

      <!-- Primary Contact Section -->
      <div class="border-t border-slate-200 pt-6">
        <h3 class="text-slate-700 font-medium mb-4">
          {{ attending ? 'Your Details' : 'Contact Details' }}
        </h3>

        <div class="space-y-4">
          <div>
            <label for="name" class="block text-slate-600 text-sm mb-1">Your Name</label>
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
            <label for="email" class="block text-slate-600 text-sm mb-1">Email Address</label>
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
            <label for="postal-address" class="block text-slate-600 text-sm mb-1">Postal Address</label>
            <textarea
              id="postal-address"
              v-model="postalAddress"
              class="input-field"
              rows="2"
              placeholder="Your mailing address"
            ></textarea>
            <p class="text-slate-400 text-xs mt-1">This will be used to mail you a save the date and formal invitation.</p>
          </div>

          <div v-if="attending">
            <label for="dietary" class="block text-slate-600 text-sm mb-1">
              Dietary Requirements <span class="text-slate-400">(optional)</span>
            </label>
            <input
              id="dietary"
              v-model="dietaryRequirements"
              type="text"
              class="input-field"
              placeholder="e.g., Vegetarian, Gluten-free, Nut allergy"
            />
          </div>
        </div>
      </div>

      <!-- Additional Guests Section -->
      <div class="border-t border-slate-200 pt-6">
        <div class="flex items-center justify-between mb-4">
          <h3 class="text-slate-700 font-medium">
            Additional Guests
            <span class="text-slate-400 font-normal text-sm">({{ totalGuestCount }}/{{ MAX_GUESTS }} total)</span>
          </h3>
          <button
            v-if="canAddMoreGuests"
            type="button"
            @click="addGuest"
            class="text-blue-500 hover:text-blue-600 text-sm font-medium flex items-center gap-1"
          >
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
            </svg>
            Add Guest
          </button>
        </div>

        <div v-if="additionalGuests.length === 0" class="text-slate-400 text-sm py-4 text-center">
          {{ attending ? 'RSVPing just for yourself? Click "Add Guest" to include family members or friends.' : 'Click "Add Guest" to include others who can\'t attend.' }}
        </div>

        <div class="space-y-4">
          <div
            v-for="(guest, index) in additionalGuests"
            :key="index"
            class="p-4 bg-slate-50 rounded-lg relative"
          >
            <button
              type="button"
              @click="removeGuest(index)"
              class="absolute top-2 right-2 text-slate-400 hover:text-red-500 transition-colors"
              title="Remove guest"
            >
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>

            <div class="text-sm text-slate-500 mb-2">Guest {{ index + 2 }}</div>

            <div class="space-y-3">
              <div>
                <label :for="'guest-name-' + index" class="block text-slate-600 text-sm mb-1">Name</label>
                <input
                  :id="'guest-name-' + index"
                  v-model="guest.name"
                  type="text"
                  class="input-field"
                  placeholder="Guest's full name"
                  required
                />
              </div>

              <div v-if="attending">
                <label :for="'guest-dietary-' + index" class="block text-slate-600 text-sm mb-1">
                  Dietary Requirements <span class="text-slate-400">(optional)</span>
                </label>
                <input
                  :id="'guest-dietary-' + index"
                  v-model="guest.dietaryRequirements"
                  type="text"
                  class="input-field"
                  placeholder="e.g., Vegetarian, Gluten-free"
                />
              </div>
            </div>
          </div>
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
        <span v-else>
          Submit RSVP for {{ totalGuestCount }} {{ totalGuestCount === 1 ? 'Guest' : 'Guests' }}
        </span>
      </button>

      <div class="mt-6 p-4 bg-amber-50 border border-amber-200 rounded-lg text-center">
        <p class="text-amber-800 text-sm font-medium">
          Please check your spam/junk folder if you don't receive a confirmation email.
        </p>
      </div>
    </form>
  </div>
</template>
