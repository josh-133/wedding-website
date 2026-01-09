<script setup>
import AppHeader from './components/layout/AppHeader.vue'
import AppFooter from './components/layout/AppFooter.vue'
</script>

<template>
  <div class="min-h-screen flex flex-col romantic-gradient">
    <AppHeader />
    <main class="flex-grow">
      <router-view />
    </main>
    <AppFooter />
  </div>
</template>
