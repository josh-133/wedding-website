<script setup>
const currentYear = new Date().getFullYear()
</script>

<template>
  <footer class="bg-white border-t border-slate-200 py-8 mt-auto">
    <div class="max-w-6xl mx-auto px-4 text-center">
      <p class="font-serif text-2xl text-blue-500 mb-2">Isabella & Joshua</p>
      <p class="text-slate-400 text-sm">
        &copy; {{ currentYear }} &middot; Made with love
      </p>
    </div>
  </footer>
</template>
