<template>
  <div class="signup-list">
    <div class="filters">
      <el-date-picker
        v-model="filterDate"
        type="date"
        placeholder="选择日期"
        value-format="YYYY-MM-DD"
        size="small"
        clearable
        @change="loadSignups"
      />
      <el-select v-model="filterShift" placeholder="选择班次" size="small" clearable @change="loadSignups">
        <el-option label="第一班次 13:30-15:30" value="13:30-15:30" />
        <el-option label="第二班次 15:30-17:30" value="15:30-17:30" />
      </el-select>
    </div>

    <div class="list">
      <div v-if="signups.length === 0" class="empty">暂无数据</div>
      <div v-for="item in signups" :key="item.id" class="list-item">
        <div class="item-left">
          <div class="shift-tag" :class="item.shift === '13:30-15:30' ? 'tag-blue' : 'tag-teal'">
            {{ item.shift === '13:30-15:30' ? '一' : '二' }}
          </div>
          <div class="item-info">
            <div class="item-name">{{ item.name }}</div>
            <div class="item-meta">{{ item.date }} · {{ item.shift }}</div>
          </div>
        </div>
        <el-button type="danger" text size="small" @click="handleDelete(item.id, item.name)" class="del-btn">
          删除
        </el-button>
      </div>
    </div>

    <el-button type="primary" size="large" style="width: 100%; margin-top: 14px; border-radius: 10px;" @click="handleExport">
      导出 Excel
    </el-button>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { getAdminSignups, deleteSignup, exportExcel } from '../api'

const signups = ref([])
const filterDate = ref('')
const filterShift = ref('')

async function loadSignups() {
  const params = {}
  if (filterDate.value) params.date = filterDate.value
  if (filterShift.value) params.shift = filterShift.value
  const { data } = await getAdminSignups(params)
  signups.value = data
}

async function handleDelete(id, name) {
  try {
    await ElMessageBox.confirm(
      `确定删除「${name}」的报名记录？`,
      '删除确认',
      { type: 'warning', confirmButtonText: '删除', cancelButtonText: '取消' }
    )
    await deleteSignup(id)
    ElMessage.success('已删除')
    await loadSignups()
  } catch {
    // cancelled
  }
}

async function handleExport() {
  try {
    const params = {}
    if (filterDate.value) params.start_date = filterDate.value
    if (filterDate.value) params.end_date = filterDate.value
    const { data } = await exportExcel(params)
    const url = URL.createObjectURL(data)
    const a = document.createElement('a')
    a.href = url
    a.download = `repair_signups_${new Date().toISOString().slice(0, 10)}.xlsx`
    a.click()
    URL.revokeObjectURL(url)
  } catch {
    ElMessage.error('导出失败')
  }
}

onMounted(loadSignups)
</script>

<style scoped>
.signup-list {
  background: #fff;
  border-radius: 14px;
  padding: 16px;
  box-shadow: 0 1px 4px rgba(0,0,0,0.04);
  border: 1px solid #f0f0f0;
}
.filters {
  display: flex;
  gap: 8px;
  margin-bottom: 14px;
}
.empty {
  text-align: center;
  color: #ccc;
  padding: 36px 0;
  font-size: 14px;
}
.list-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 0;
  border-bottom: 1px solid #f5f5f5;
}
.list-item:last-child {
  border-bottom: none;
}
.item-left {
  display: flex;
  align-items: center;
  gap: 10px;
}
.shift-tag {
  width: 28px;
  height: 28px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 12px;
  font-weight: 700;
  color: #fff;
  flex-shrink: 0;
}
.tag-blue {
  background: linear-gradient(135deg, #667eea, #764ba2);
}
.tag-teal {
  background: linear-gradient(135deg, #13c2c2, #667eea);
}
.item-name {
  font-size: 14px;
  font-weight: 600;
  color: #1a1a2e;
}
.item-meta {
  font-size: 11px;
  color: #bbb;
  margin-top: 2px;
}
.del-btn {
  color: #ccc !important;
  font-size: 12px;
}
.del-btn:hover {
  color: #f56c6c !important;
}
</style>
