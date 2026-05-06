<template>
  <div class="chart-container">
    <h3 class="chart-title">每周报名趋势</h3>
    <div style="height: 250px; display: flex; align-items: center; justify-content: center; color: #999;">
      图表加载中...
    </div>
  </div>
</template>

<script setup>
defineProps({ trend: Array })
</script>

<style scoped>
.chart-container {
  background: white;
  border-radius: 12px;
  padding: 16px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.08);
}
.chart-title {
  font-size: 15px;
  font-weight: 500;
  color: #333;
  margin-bottom: 12px;
}
</style>
