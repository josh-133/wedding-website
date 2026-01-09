<script setup>
import { ref, onMounted } from 'vue'
import { getRegistry } from '../api'
import QrCodeDisplay from '../components/registry/QrCodeDisplay.vue'

const registryUrl = ref('')
const loading = ref(true)
const error = ref('')

onMounted(async () => {
  try {
    const response = await getRegistry()
    registryUrl.value = response.data.registry_url
  } catch (err) {
    error.value = 'Failed to load registry information'
    console.error('Failed to load registry:', err)
  } finally {
    loading.value = false
  }
})
</script>

<template>
  <div class="py-12 px-4">
    <div class="max-w-4xl mx-auto text-center mb-8">
      <router-link to="/" class="text-blue-400 hover:text-blue-500 text-sm mb-4 inline-block">
        &larr; Back to Home
      </router-link>
    </div>

    <div class="card max-w-lg mx-auto text-center">
      <h1 class="font-serif text-3xl text-slate-800 mb-4">Our Registry</h1>
      <p class="text-slate-600 mb-8">
        Your presence at our celebration is the greatest gift of all.
        However, if you wish to honour us with a gift, we've created a registry
        with a few items we'd love.
      </p>

      <div v-if="loading" class="py-12">
        <div class="animate-pulse text-blue-400">Loading registry...</div>
      </div>

      <div v-else-if="error" class="py-8 text-red-500">
        {{ error }}
      </div>

      <template v-else>
        <QrCodeDisplay :url="registryUrl" />

        <div class="mt-8">
          <p class="text-slate-400 text-sm mb-4">Or visit directly:</p>
          <a
            :href="registryUrl"
            target="_blank"
            rel="noopener noreferrer"
            class="btn-primary inline-block"
          >
            View Registry
          </a>
        </div>
      </template>
    </div>
  </div>
</template>
