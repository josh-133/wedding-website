<script setup>
import { ref, onMounted } from 'vue'
import { getEvents } from '../api'

const events = ref([])
const loading = ref(true)

// FAQ accordion state
const openFaq = ref(null)

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

// Schedule information
const scheduleInfo = {
  engagement: {
    date: 'Saturday, 23rd May 2026',
    time: '4:00 PM - 8:00 PM',
    details: 'Join us for an afternoon of celebration'
  },
  wedding: {
    date: 'Saturday, 22nd May 2027',
    ceremonyTime: '2:30 PM for a 3:00 PM start',
    receptionTime: '5:00 PM - Midnight',
    details: 'Ceremony followed by cocktail hour and reception dinner'
  }
}

// Venue information
const venueInfo = {
  engagement: {
    name: 'Beefacres Hall',
    address: '14 Pittwater Dr',
    city: 'Windsor Gardens SA 5087',
    mapsUrl: 'https://maps.google.com/?q=14+Pittwater+Dr,+Windsor+Gardens+SA+5087',
    mapsEmbed: 'https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3271.5!2d138.6647!3d-34.8547!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x6ab0b8e5c5c5c5c5%3A0x0!2s14%20Pittwater%20Dr%2C%20Windsor%20Gardens%20SA%205087!5e0!3m2!1sen!2sau!4v1234567890',
    parking: 'On-site parking available',
    notes: ''
  },
  wedding: {
    name: 'Mount Lofty House',
    address: '1 Mawson Dr',
    city: 'Crafers SA 5152',
    mapsUrl: 'https://maps.google.com/?q=1+Mawson+Dr,+Crafers+SA+5152',
    mapsEmbed: 'https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3271.5!2d138.7089!3d-34.9789!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x6ab0cea1e8e8e8e8%3A0x0!2sMount%20Lofty%20House%2C%201%20Mawson%20Dr%2C%20Crafers%20SA%205152!5e0!3m2!1sen!2sau!4v1234567890',
    parking: 'On-site parking available',
    accommodation: 'Accommodation available at Mount Lofty House - contact venue directly to book'
  }
}

// Dress code information (shared for both events)
const dressCodeInfo = {
  code: 'Garden Party Formal',
  description: 'Attire is Garden Party Formal. If you\'d like to embrace the theme further, feel free to be imaginative with bright & pastel colors, florals, etc, but any daytime formal attire is appropriate. We suggest lightweight suits for men and airy long dresses for women. We kindly ask ladies to avoid wearing blue so as not to match our bridesmaids.',
  images: [
    { src: '/images/outfit-inspiration-1.jpg', alt: 'Outfit inspiration 1' },
    { src: '/images/outfit-inspiration-2.jpg', alt: 'Outfit inspiration 2' },
    { src: '/images/outfit-inspiration-3.jpg', alt: 'Outfit inspiration 3' }
  ]
}

// FAQ items
const faqItems = [
  {
    question: 'Can I bring a plus one?',
    answer: 'If you\'ve been given a plus one, a separate invitation will be sent to them. If you have any questions, please don\'t hesitate to reach out to us.'
  },
  {
    question: 'Are children welcome?',
    answer: 'While we love your little ones, our wedding will be an adults-only celebration. We hope this gives you a chance to enjoy a night out! The only exceptions will be made for family travelling from afar.'
  },
  {
    question: 'When is the RSVP deadline?',
    answer: 'Please RSVP for the wedding by 31st March 2027 so we can finalize catering and seating arrangements.'
  },
  {
    question: 'Is there accommodation nearby?',
    answer: 'If you would like to book accommodation, please contact our wedding coordinator Crystal Bihun on 08 8130 9237 or wedding.coordinator@mtloftyhouse.com.au for further information.'
  },
  {
    question: 'What time should I arrive?',
    answer: 'Please arrive 15-30 minutes before the ceremony start time to find your seats.'
  }
]

function formatDate(dateStr) {
  const date = new Date(dateStr)
  return date.toLocaleDateString('en-AU', {
    weekday: 'long',
    day: 'numeric',
    month: 'long',
    year: 'numeric'
  })
}

function toggleFaq(index) {
  openFaq.value = openFaq.value === index ? null : index
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
  <div>
    <!-- Hero/Welcome Section - Light Blue -->
    <section class="bg-blue-50 py-16 px-4">
      <div class="max-w-4xl mx-auto text-center">
        <div class="flex items-center justify-center gap-3 mb-4">
          <span class="text-sage-400 text-lg">🌿</span>
          <p class="text-sage-500 uppercase tracking-widest text-sm">You're Invited</p>
          <span class="text-sage-400 text-lg">🌿</span>
        </div>
        <h1 class="font-serif text-5xl md:text-6xl text-slate-800 mb-4">
          Isabella & Joshua
        </h1>
        <p class="text-lg text-slate-600 max-w-2xl mx-auto leading-relaxed">
          Thank you for being part of our story. We're so grateful to have you in our lives
          and can't wait to celebrate these special moments with you. Your presence means
          the world to us!
        </p>
      </div>
    </section>

    <!-- Our Celebrations Section - Light Pink -->
    <section class="bg-pink-50 py-16 px-4">
      <div class="max-w-6xl mx-auto">
        <h2 class="font-serif text-3xl text-slate-800 text-center mb-8">Our Celebrations</h2>

        <div v-if="loading" class="text-center py-12">
          <div class="animate-pulse text-blue-400">Loading events...</div>
        </div>

        <div v-else class="grid md:grid-cols-2 gap-8">
          <!-- Engagement Party (Left) -->
          <div class="card flex flex-col bg-white/80 border-blush-100">
            <div class="text-center mb-6">
              <span class="text-4xl mb-3 block">💍</span>
              <h3 class="font-serif text-2xl text-slate-800 mb-2">Engagement Party</h3>
              <p class="text-blue-500 font-medium">{{ scheduleInfo.engagement.date }}</p>
              <p class="text-slate-600">{{ scheduleInfo.engagement.time }}</p>
            </div>

            <div class="mb-6">
              <p class="font-medium text-slate-800 text-lg">{{ venueInfo.engagement.name }}</p>
              <p class="text-slate-600">{{ venueInfo.engagement.address }}</p>
              <p class="text-slate-600 mb-3">{{ venueInfo.engagement.city }}</p>

              <div class="bg-slate-100 rounded-lg overflow-hidden aspect-video mb-3">
                <iframe
                  :src="venueInfo.engagement.mapsEmbed"
                  width="100%"
                  height="100%"
                  style="border:0; min-height: 180px;"
                  allowfullscreen=""
                  loading="lazy"
                  referrerpolicy="no-referrer-when-downgrade"
                  class="w-full h-full"
                ></iframe>
              </div>

              <a
                :href="venueInfo.engagement.mapsUrl"
                target="_blank"
                rel="noopener noreferrer"
                class="inline-flex items-center gap-2 text-blue-500 hover:text-blue-600 font-medium text-sm"
              >
                <span>📍</span> Get Directions
              </a>
            </div>

            <div class="mb-6">
              <p class="text-sm text-slate-600 mb-2">{{ scheduleInfo.engagement.details }}</p>
              <div class="space-y-1 text-sm text-slate-600">
                <p><span class="font-medium">Parking:</span> {{ venueInfo.engagement.parking }}</p>
              </div>
            </div>

            <!-- RSVP Button -->
            <div class="mt-auto text-center">
              <router-link
                to="/engagement"
                class="btn-primary inline-block w-full py-3"
              >
                RSVP for Engagement Party
              </router-link>
            </div>
          </div>

          <!-- Wedding (Right) -->
          <div class="card flex flex-col bg-white/80 border-lavender-100">
            <div class="text-center mb-6">
              <span class="text-4xl mb-3 block">💒</span>
              <h3 class="font-serif text-2xl text-slate-800 mb-2">Wedding Day</h3>
              <p class="text-blue-500 font-medium">{{ scheduleInfo.wedding.date }}</p>
              <p class="text-slate-600">Ceremony: {{ scheduleInfo.wedding.ceremonyTime }} | Reception: {{ scheduleInfo.wedding.receptionTime }}</p>
            </div>

            <div class="mb-6">
              <p class="font-medium text-slate-800 text-lg">{{ venueInfo.wedding.name }}</p>
              <p class="text-slate-600">{{ venueInfo.wedding.address }}</p>
              <p class="text-slate-600 mb-3">{{ venueInfo.wedding.city }}</p>

              <div class="bg-slate-100 rounded-lg overflow-hidden aspect-video mb-3">
                <iframe
                  :src="venueInfo.wedding.mapsEmbed"
                  width="100%"
                  height="100%"
                  style="border:0; min-height: 180px;"
                  allowfullscreen=""
                  loading="lazy"
                  referrerpolicy="no-referrer-when-downgrade"
                  class="w-full h-full"
                ></iframe>
              </div>

              <a
                :href="venueInfo.wedding.mapsUrl"
                target="_blank"
                rel="noopener noreferrer"
                class="inline-flex items-center gap-2 text-blue-500 hover:text-blue-600 font-medium text-sm"
              >
                <span>📍</span> Get Directions
              </a>
            </div>

            <div class="mb-6">
              <p class="text-sm text-slate-600 mb-2">{{ scheduleInfo.wedding.details }}</p>
              <div class="space-y-1 text-sm text-slate-600">
                <p><span class="font-medium">Parking:</span> {{ venueInfo.wedding.parking }}</p>
                <p v-if="venueInfo.wedding.accommodation"><span class="font-medium">Accommodation:</span> {{ venueInfo.wedding.accommodation }}</p>
              </div>
            </div>

            <!-- RSVP Button -->
            <div class="mt-auto text-center">
              <router-link
                to="/wedding"
                class="btn-primary inline-block w-full py-3"
              >
                RSVP for Wedding
              </router-link>
            </div>
          </div>
        </div>

        <!-- Shared Dress Code Section -->
        <div class="mt-8 p-6 bg-white/80 rounded-xl text-center max-w-4xl mx-auto border border-sage-100">
          <div class="flex items-center justify-center gap-2 mb-3">
            <span class="text-sage-500 text-xl">🌸</span>
            <span class="font-serif text-xl text-slate-800">Dress Code</span>
            <span class="bg-sage-100 text-sage-600 px-3 py-1 rounded-full text-sm font-medium">
              {{ dressCodeInfo.code }}
            </span>
          </div>
          <p class="text-sm text-sage-500 font-medium mb-3">For both the Engagement Party & Wedding</p>
          <p class="text-slate-600">{{ dressCodeInfo.description }}</p>
        </div>
      </div>
    </section>

    <!-- Registry Section - Light Green -->
    <section class="bg-green-50 py-16 px-4">
      <div class="max-w-4xl mx-auto text-center">
        <span class="text-5xl mb-6 block">🎁</span>
        <h2 class="font-serif text-3xl text-slate-800 mb-4">Gift Registry</h2>
        <p class="text-lg text-slate-600 mb-6 max-w-xl mx-auto">
          Your presence at our wedding is the greatest gift of all. However, if you wish to honour us with a gift, we have created a registry for your convenience.
        </p>
        <router-link to="/registry" class="btn-primary inline-block text-lg px-8 py-3">
          View Registry
        </router-link>
      </div>
    </section>

    <!-- FAQ Section - Light Purple -->
    <section id="faq" class="bg-purple-50 py-16 px-4 scroll-mt-24">
      <div class="max-w-4xl mx-auto">
        <h2 class="font-serif text-3xl text-slate-800 text-center mb-8">Frequently Asked Questions</h2>

        <div class="space-y-4">
          <div
            v-for="(faq, index) in faqItems"
            :key="index"
            class="bg-white/80 rounded-xl shadow-sm overflow-hidden"
          >
            <button
              @click="toggleFaq(index)"
              class="w-full px-6 py-4 text-left flex items-center justify-between hover:bg-white transition-colors"
            >
              <span class="font-medium text-slate-800">{{ faq.question }}</span>
              <span
                class="text-blue-400 transition-transform duration-200"
                :class="{ 'rotate-180': openFaq === index }"
              >
                ▼
              </span>
            </button>
            <div
              v-show="openFaq === index"
              class="px-6 pb-4 text-slate-600"
            >
              {{ faq.answer }}
            </div>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>
