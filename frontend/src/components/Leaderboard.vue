<template>
  <div class="leaderboard">
    <div v-if="!data || data.length === 0" class="empty">暂无数据</div>
    <div v-else>
      <div
        v-for="(item, index) in data"
        :key="item.name"
        class="lb-item"
      >
        <div class="lb-rank" :class="{ top3: index < 3 }">{{ index + 1 }}</div>
        <div class="lb-name">{{ item.name }}</div>
        <div class="lb-count">{{ item.count }} 次</div>
      </div>
    </div>
  </div>
</template>

<script setup>
defineProps({ data: Array })
</script>

<style scoped>
.leaderboard {
  background: white;
  border-radius: 12px;
  padding: 16px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.08);
}
.empty {
  text-align: center;
  color: #999;
  padding: 32px;
}
.lb-item {
  display: flex;
  align-items: center;
  padding: 12px 0;
  border-bottom: 1px solid #f5f5f5;
}
.lb-item:last-child {
  border-bottom: none;
}
.lb-rank {
  width: 28px;
  height: 28px;
  border-radius: 50%;
  background: #f0f0f0;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 13px;
  font-weight: 600;
  color: #666;
  margin-right: 12px;
}
.lb-rank.top3 {
  background: #fff7e6;
  color: #fa8c16;
}
.lb-name {
  flex: 1;
  font-size: 15px;
  color: #333;
}
.lb-count {
  font-size: 14px;
  color: #1890ff;
  font-weight: 500;
}
</style>
