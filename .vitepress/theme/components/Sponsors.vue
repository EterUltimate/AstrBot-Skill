<template>
  <div class="sponsors">
    <div class="wwads-cn wwads-vertical wwads-sticky" data-id="380" style="max-width:180px"></div>
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
  padding: 24px;
  border-radius: 8px;
  font-size: 11px;
  display: flex;
  justify-content: center;
  align-items: center;
  flex-direction: column;
  gap: 8px;
}
</style>