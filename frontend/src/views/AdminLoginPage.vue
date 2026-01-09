<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import { adminLogin } from '../api'

const router = useRouter()
const authStore = useAuthStore()

const password = ref('')
const isSubmitting = ref(false)
const error = ref('')

async function handleLogin() {
  if (!password.value) {
    error.value = 'Please enter a password'
    return
  }

  isSubmitting.value = true
  error.value = ''

  try {
    const response = await adminLogin(password.value)
    authStore.setToken(response.data.access_token)
    router.push('/admin/dashboard')
  } catch (err) {
    error.value = err.response?.data?.detail || 'Invalid password'
  } finally {
    isSubmitting.value = false
  }
}
</script>

<template>
  <div class="py-12 px-4">
    <div class="card max-w-sm mx-auto">
      <div class="text-center mb-8">
        <h1 class="font-serif text-2xl text-gray-800 mb-2">Admin Login</h1>
        <p class="text-gray-500 text-sm">Enter the admin password to continue</p>
      </div>

      <form @submit.prevent="handleLogin" class="space-y-6">
        <div>
          <label for="password" class="block text-gray-700 font-medium mb-2">Password</label>
          <input
            id="password"
            v-model="password"
            type="password"
            class="input-field"
            placeholder="Enter password"
            autocomplete="current-password"
          />
        </div>

        <div v-if="error" class="p-4 bg-red-50 border border-red-200 rounded-lg text-red-600 text-sm">
          {{ error }}
        </div>

        <button
          type="submit"
          :disabled="isSubmitting"
          class="btn-primary w-full disabled:opacity-50 disabled:cursor-not-allowed"
        >
          <span v-if="isSubmitting">Logging in...</span>
          <span v-else>Login</span>
        </button>
      </form>
    </div>
  </div>
</template>
