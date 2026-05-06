<template>
  <div class="stats-grid">
    <div class="stat-card">
      <div class="stat-icon blue-bg">&#128200;</div>
      <div class="stat-content">
        <div class="stat-label">本周报名</div>
        <div class="stat-value blue">{{ stats.week_count }}</div>
      </div>
    </div>
    <div class="stat-card">
      <div class="stat-icon purple-bg">&#128101;</div>
      <div class="stat-content">
        <div class="stat-label">累计参与</div>
        <div class="stat-value purple">{{ stats.total_count }}</div>
      </div>
    </div>
    <div class="stat-card">
      <div class="stat-icon orange-bg">&#128336;</div>
      <div class="stat-content">
        <div class="stat-label">第一班次</div>
        <div class="stat-value orange">{{ stats.shift1_count }}</div>
        <div class="stat-sub">13:30-15:30</div>
      </div>
    </div>
    <div class="stat-card">
      <div class="stat-icon teal-bg">&#128337;</div>
      <div class="stat-content">
        <div class="stat-label">第二班次</div>
        <div class="stat-value teal">{{ stats.shift2_count }}</div>
        <div class="stat-sub">15:30-17:30</div>
      </div>
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
  background: #fff;
  border-radius: 14px;
  padding: 16px;
  display: flex;
  align-items: center;
  gap: 12px;
  box-shadow: 0 1px 4px rgba(0,0,0,0.04);
  border: 1px solid #f0f0f0;
}
.stat-icon {
  width: 40px;
  height: 40px;
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 18px;
  flex-shrink: 0;
}
.blue-bg { background: linear-gradient(135deg, #667eea20, #667eea10); }
.purple-bg { background: linear-gradient(135deg, #764ba220, #764ba210); }
.orange-bg { background: linear-gradient(135deg, #fa8c1620, #fa8c1610); }
.teal-bg { background: linear-gradient(135deg, #13c2c220, #13c2c210); }
.stat-content {
  min-width: 0;
}
.stat-label {
  font-size: 11px;
  color: #999;
  letter-spacing: 0.3px;
}
.stat-value {
  font-size: 28px;
  font-weight: 700;
  margin-top: 2px;
  line-height: 1.1;
}
.stat-sub {
  font-size: 10px;
  color: #bbb;
  margin-top: 2px;
}
.blue { color: #667eea; }
.purple { color: #764ba2; }
.orange { color: #fa8c16; }
.teal { color: #13c2c2; }
</style>
