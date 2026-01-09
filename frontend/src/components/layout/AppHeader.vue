<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../../stores/auth'

const router = useRouter()
const authStore = useAuthStore()
const mobileMenuOpen = ref(false)

const navLinks = [
  { name: 'Home', path: '/' },
  { name: 'Engagement', path: '/engagement' },
  { name: 'Wedding', path: '/wedding' },
  { name: 'Registry', path: '/registry' },
]

function handleLogout() {
  authStore.logout()
  router.push('/')
}
</script>

<template>
  <header class="bg-white/90 backdrop-blur-sm border-b border-slate-200 sticky top-0 z-50">
    <nav class="max-w-6xl mx-auto px-4 py-4">
      <div class="flex justify-between items-center">
        <router-link to="/" class="font-serif text-2xl text-blue-500 hover:text-blue-600 transition-colors">
          I & J
        </router-link>

        <!-- Desktop Navigation -->
        <div class="hidden md:flex items-center gap-8">
          <router-link
            v-for="link in navLinks"
            :key="link.path"
            :to="link.path"
            class="text-slate-600 hover:text-blue-500 transition-colors font-medium"
            active-class="text-blue-500"
          >
            {{ link.name }}
          </router-link>
          <template v-if="authStore.isAuthenticated">
            <router-link
              to="/admin/dashboard"
              class="text-slate-600 hover:text-blue-500 transition-colors font-medium"
              active-class="text-blue-500"
            >
              Dashboard
            </router-link>
            <button
              @click="handleLogout"
              class="text-slate-400 hover:text-blue-500 text-sm"
            >
              Logout
            </button>
          </template>
        </div>

        <!-- Mobile Menu Button -->
        <button
          @click="mobileMenuOpen = !mobileMenuOpen"
          class="md:hidden p-2 text-slate-600"
        >
          <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path
              v-if="!mobileMenuOpen"
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="2"
              d="M4 6h16M4 12h16M4 18h16"
            />
            <path
              v-else
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="2"
              d="M6 18L18 6M6 6l12 12"
            />
          </svg>
        </button>
      </div>

      <!-- Mobile Navigation -->
      <div v-if="mobileMenuOpen" class="md:hidden mt-4 pb-4 space-y-3">
        <router-link
          v-for="link in navLinks"
          :key="link.path"
          :to="link.path"
          @click="mobileMenuOpen = false"
          class="block text-slate-600 hover:text-blue-500 transition-colors font-medium py-2"
          active-class="text-blue-500"
        >
          {{ link.name }}
        </router-link>
        <template v-if="authStore.isAuthenticated">
          <router-link
            to="/admin/dashboard"
            @click="mobileMenuOpen = false"
            class="block text-slate-600 hover:text-blue-500 transition-colors font-medium py-2"
          >
            Dashboard
          </router-link>
          <button
            @click="handleLogout; mobileMenuOpen = false"
            class="block text-slate-400 hover:text-blue-500 text-sm py-2"
          >
            Logout
          </button>
        </template>
      </div>
    </nav>
  </header>
</template>
