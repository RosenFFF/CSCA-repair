<template>
  <div class="leaderboard">
    <div v-if="!data || data.length === 0" class="empty">暂无数据</div>
    <div v-else>
      <div
        v-for="(item, index) in data"
        :key="item.name"
        class="lb-item"
      >
        <div class="lb-rank" :class="{ top1: index === 0, top2: index === 1, top3: index === 2 }">
          {{ index + 1 }}
        </div>
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
  background: #fff;
  border-radius: 14px;
  padding: 16px;
  box-shadow: 0 1px 4px rgba(0,0,0,0.04);
  border: 1px solid #f0f0f0;
}
.empty {
  text-align: center;
  color: #ccc;
  padding: 36px 0;
  font-size: 14px;
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
  width: 30px;
  height: 30px;
  border-radius: 10px;
  background: #f0f2f5;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 13px;
  font-weight: 700;
  color: #999;
  margin-right: 12px;
  flex-shrink: 0;
}
.lb-rank.top1 {
  background: linear-gradient(135deg, #667eea, #764ba2);
  color: #fff;
}
.lb-rank.top2 {
  background: linear-gradient(135deg, #667eea, #13c2c2);
  color: #fff;
}
.lb-rank.top3 {
  background: linear-gradient(135deg, #fa8c16, #fadb14);
  color: #fff;
}
.lb-name {
  flex: 1;
  font-size: 14px;
  font-weight: 600;
  color: #1a1a2e;
}
.lb-count {
  font-size: 13px;
  color: #667eea;
  font-weight: 600;
}
</style>
