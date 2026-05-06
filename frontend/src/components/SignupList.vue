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
        <el-option label="13:30-15:30" value="13:30-15:30" />
        <el-option label="15:30-17:30" value="15:30-17:30" />
      </el-select>
    </div>

    <div class="list">
      <div v-if="signups.length === 0" class="empty">暂无数据</div>
      <div v-for="item in signups" :key="item.id" class="list-item">
        <div class="item-info">
          <div class="item-name">{{ item.name }}</div>
          <div class="item-meta">{{ item.date }} · {{ item.shift }}</div>
        </div>
        <el-button type="danger" text size="small" @click="handleDelete(item.id)">删除</el-button>
      </div>
    </div>

    <el-button type="success" size="large" style="width: 100%; margin-top: 12px" @click="handleExport">
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

async function handleDelete(id) {
  try {
    await ElMessageBox.confirm('确定删除这条记录？', '提示', { type: 'warning' })
    await deleteSignup(id)
    ElMessage.success('删除成功')
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
  background: white;
  border-radius: 12px;
  padding: 16px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.08);
}
.filters {
  display: flex;
  gap: 8px;
  margin-bottom: 12px;
}
.empty {
  text-align: center;
  color: #999;
  padding: 32px;
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
.item-name {
  font-size: 15px;
  font-weight: 500;
  color: #333;
}
.item-meta {
  font-size: 12px;
  color: #999;
  margin-top: 2px;
}
</style>
