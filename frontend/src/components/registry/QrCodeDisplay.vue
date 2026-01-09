<script setup>
import { ref, onMounted, watch } from 'vue'
import QrcodeVue from 'qrcode-vue3'

const props = defineProps({
  url: {
    type: String,
    required: true
  }
})

const size = ref(250)
</script>

<template>
  <div class="flex flex-col items-center">
    <div class="bg-white p-6 rounded-2xl shadow-lg">
      <QrcodeVue
        :value="url"
        :size="size"
        level="M"
        render-as="svg"
        :margin="2"
        :image-options="{ hideBackgroundDots: true, imageSize: 0.4, margin: 10 }"
      />
    </div>
    <p class="mt-4 text-gray-500 text-sm">Scan to view our registry</p>
  </div>
</template>
