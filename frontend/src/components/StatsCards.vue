<template>
  <div class="stats-grid">
    <div class="stat-card blue">
      <div class="stat-label">本周报名</div>
      <div class="stat-value">{{ stats.week_count }}</div>
    </div>
    <div class="stat-card purple">
      <div class="stat-label">累计参与</div>
      <div class="stat-value">{{ stats.total_count }}</div>
    </div>
    <div class="stat-card orange">
      <div class="stat-label">第一班次</div>
      <div class="stat-value">{{ stats.shift1_count }}</div>
      <div class="stat-sub">13:30-15:30</div>
    </div>
    <div class="stat-card teal">
      <div class="stat-label">第二班次</div>
      <div class="stat-value">{{ stats.shift2_count }}</div>
      <div class="stat-sub">15:30-17:30</div>
    </div>
  </div>
</template>

<script setup>
defineProps({ stats: Object })
</script>

<style scoped>
.stats-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 10px;
  margin-bottom: 16px;
}
.stat-card {
  background: white;
  border-radius: 12px;
  padding: 16px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.08);
}
.stat-label {
  font-size: 12px;
  color: #999;
}
.stat-value {
  font-size: 32px;
  font-weight: 700;
  margin-top: 4px;
}
.stat-sub {
  font-size: 11px;
  color: #999;
  margin-top: 2px;
}
.blue .stat-value { color: #1890ff; }
.purple .stat-value { color: #722ed1; }
.orange .stat-value { color: #fa8c16; }
.teal .stat-value { color: #13c2c2; }
</style>
