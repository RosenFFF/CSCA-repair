<template>
  <div class="activity-card" :class="{ full: activity.is_full }">
    <div class="card-header">
      <span class="shift-label">{{ activity.shift }}</span>
      <span class="count" :class="{ 'count-full': activity.is_full }">
        {{ activity.signup_count }}/{{ activity.max_signup }}
      </span>
    </div>
    <el-button
      v-if="!activity.is_full"
      type="primary"
      size="large"
      round
      @click="$emit('signup', activity)"
    >
      报名
    </el-button>
    <el-button v-else type="info" size="large" round disabled>
      已满
    </el-button>
  </div>
</template>

<script setup>
defineProps({ activity: Object })
defineEmits(['signup'])
</script>

<style scoped>
.activity-card {
  background: white;
  border-radius: 12px;
  padding: 16px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.08);
}
.activity-card.full {
  opacity: 0.6;
}
.card-header {
  display: flex;
  flex-direction: column;
  gap: 4px;
}
.shift-label {
  font-size: 15px;
  font-weight: 500;
  color: #333;
}
.count {
  font-size: 13px;
  color: #999;
}
.count-full {
  color: #f56c6c;
}
</style>
