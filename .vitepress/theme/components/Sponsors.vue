<template>
  <div>
    <div class="wwads-cn wwads-vertical sponsors" data-id="380" style="max-width:180px"></div>
  </div>
</template>

<script setup>
import { onMounted } from 'vue'

onMounted(() => {
  const script = document.createElement('script')
  script.src = 'https://cdn.wwads.cn/js/makemoney.js'
  script.async = true
  document.head.appendChild(script)
})
</script>

<style scoped>
.sponsors {
  max-width: 100%;
  margin: 0 !important;
  background-color: transparent !important;
}

.sponsors .wwads-text {
  color: var(--vp-c-bg) !important;
  transition-property: color;
  transition-duration: 500ms;
  transition-timing-function: cubic-bezier(0.4, 0, 0.2, 1);
}
</style>