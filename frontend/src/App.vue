<script setup>
import AppHeader from './components/layout/AppHeader.vue'
import AppFooter from './components/layout/AppFooter.vue'
</script>

<template>
  <div class="min-h-screen flex flex-col romantic-gradient overflow-x-hidden">
    <!-- Decorative botanical elements -->
    <div class="leaf-decoration leaf-left hidden lg:block"></div>
    <div class="leaf-decoration leaf-right hidden lg:block"></div>

    <AppHeader />
    <main class="flex-grow relative z-10">
      <router-view />
    </main>
    <AppFooter />
  </div>
</template>
