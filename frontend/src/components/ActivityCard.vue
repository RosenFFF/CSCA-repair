<template>
  <div class="activity-card" :class="{ full: activity.is_full }">
    <div class="card-left">
      <div class="shift-badge" :class="{ 'badge-full': activity.is_full }">
        {{ shiftTitle || '班次' }}
      </div>
      <div class="card-info">
        <span class="shift-time">{{ activity.shift }}</span>
        <span class="count" :class="{ 'count-full': activity.is_full }">
          {{ activity.signup_count }}/{{ activity.max_signup }} 人
        </span>
      </div>
    </div>
    <el-button
      v-if="!activity.is_full"
      type="primary"
      size="large"
      round
      @click="$emit('signup', activity)"
      class="signup-btn"
    >
      报名
    </el-button>
    <el-button v-else type="info" size="large" round disabled class="signup-btn">
      已满
    </el-button>
  </div>
</template>

<script setup>
defineProps({
  activity: Object,
  shiftTitle: String,
})
defineEmits(['signup'])
</script>

<style scoped>
.activity-card {
  background: #fff;
  border-radius: 14px;
  padding: 16px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  box-shadow: 0 1px 4px rgba(0,0,0,0.05);
  border: 1px solid #f0f0f0;
  transition: box-shadow 0.2s;
}
.activity-card:hover {
  box-shadow: 0 4px 16px rgba(102,126,234,0.1);
}
.activity-card.full {
  opacity: 0.55;
}
.card-left {
  display: flex;
  align-items: center;
  gap: 12px;
}
.shift-badge {
  background: linear-gradient(135deg, #667eea, #764ba2);
  color: #fff;
  font-size: 12px;
  font-weight: 600;
  padding: 4px 10px;
  border-radius: 6px;
  letter-spacing: 0.5px;
  white-space: nowrap;
}
.shift-badge.badge-full {
  background: linear-gradient(135deg, #999, #bbb);
}
.card-info {
  display: flex;
  flex-direction: column;
  gap: 2px;
}
.shift-time {
  font-size: 14px;
  font-weight: 600;
  color: #1a1a2e;
}
.count {
  font-size: 12px;
  color: #999;
}
.count-full {
  color: #f56c6c;
  font-weight: 500;
}
.signup-btn {
  min-width: 72px;
}
</style>
