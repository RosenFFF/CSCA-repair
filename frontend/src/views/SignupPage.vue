<template>
  <div class="signup-page">
    <div class="page-header">
      <div class="logo">&#128295;</div>
      <h1>义务维修报名</h1>
      <p class="subtitle">计算机协会 · 每周三下午</p>
    </div>

    <!-- This week -->
    <div class="section" v-if="currentWeekActivities.length">
      <h2 class="section-title">{{ formatDate(currentWeekDate) }} 义务维修</h2>
      <div class="card-list">
        <ActivityCard
          v-for="(item, idx) in currentWeekActivities"
          :key="item.date + item.shift"
          :activity="item"
          :shiftTitle="idx === 0 ? '第一班次' : '第二班次'"
          :isHistory="false"
          @signup="openSignupDialog"
        />
      </div>
    </div>

    <!-- History -->
    <div class="section" v-if="historyActivities.length">
      <el-collapse v-model="expandedHistory">
        <el-collapse-item title="历史活动" name="history">
          <div v-for="(week, idx) in historyGrouped" :key="idx" class="history-week">
            <div class="history-date">{{ formatDate(week.date) }}</div>
            <div class="card-list">
              <ActivityCard
                v-for="(item, i) in week.items"
                :key="item.shift"
                :activity="item"
                :shiftTitle="i === 0 ? '第一班次' : '第二班次'"
                :isHistory="true"
              />
            </div>
          </div>
        </el-collapse-item>
      </el-collapse>
    </div>

    <!-- Warning -->
    <div class="warning-bar">
      如果填错或误填，请及时联系部长删除
    </div>

    <!-- Admin Entry -->
    <div class="admin-entry">
      <router-link to="/admin">管理员入口</router-link>
    </div>

    <!-- Signup Dialog -->
    <el-dialog v-model="dialogVisible" title="报名" width="90%" :show-close="false">
      <el-form @submit.prevent="submitSignup">
        <el-form-item label="姓名">
          <el-input v-model="signupName" placeholder="请输入你的姓名" maxlength="20" clearable />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="submitSignup" :loading="submitting">确认报名</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { getActivities, createSignup } from '../api'
import ActivityCard from '../components/ActivityCard.vue'

const activities = ref([])
const dialogVisible = ref(false)
const selectedActivity = ref(null)
const signupName = ref('')
const submitting = ref(false)
const expandedHistory = ref([])

const currentWeekDate = computed(() => {
  if (!activities.value.length) return ''
  return activities.value[0].date
})

const currentWeekActivities = computed(() =>
  activities.value.filter((a) => a.date === currentWeekDate.value)
)

const historyActivities = computed(() =>
  activities.value.filter((a) => a.date !== currentWeekDate.value)
)

const historyGrouped = computed(() => {
  const groups = {}
  historyActivities.value.forEach((a) => {
    if (!groups[a.date]) groups[a.date] = []
    groups[a.date].push(a)
  })
  return Object.entries(groups).map(([date, items]) => ({ date, items }))
})

function formatDate(dateStr) {
  const d = new Date(dateStr)
  return `${d.getMonth() + 1}月${d.getDate()}日 周三`
}

async function loadActivities() {
  const { data } = await getActivities()
  activities.value = data
}

function openSignupDialog(activity) {
  selectedActivity.value = activity
  signupName.value = ''
  dialogVisible.value = true
}

async function submitSignup() {
  if (!signupName.value.trim()) {
    ElMessage.warning('请输入姓名')
    return
  }
  submitting.value = true
  try {
    await createSignup({
      name: signupName.value.trim(),
      date: selectedActivity.value.date,
      shift: selectedActivity.value.shift,
    })
    ElMessage.success('报名成功！')
    dialogVisible.value = false
    await loadActivities()
  } catch (err) {
    const msg = err.response?.data?.detail || '报名失败'
    ElMessage.error(msg)
  } finally {
    submitting.value = false
  }
}

onMounted(loadActivities)
</script>

<style scoped>
.signup-page {
  max-width: 480px;
  margin: 0 auto;
  padding: 20px 16px;
  min-height: 100vh;
}
.page-header {
  text-align: center;
  margin-bottom: 24px;
}
.logo {
  font-size: 36px;
  margin-bottom: 8px;
}
h1 {
  font-size: 22px;
  font-weight: 600;
  color: #1a1a1a;
}
.subtitle {
  font-size: 13px;
  color: #666;
  margin-top: 4px;
}
.section-title {
  font-size: 16px;
  font-weight: 600;
  color: #333;
  margin-bottom: 12px;
}
.card-list {
  display: flex;
  flex-direction: column;
  gap: 10px;
  margin-bottom: 16px;
}
.history-week {
  margin-bottom: 12px;
}
.history-date {
  font-size: 13px;
  color: #999;
  margin-bottom: 8px;
}
.warning-bar {
  background: #fffbe6;
  border: 1px solid #ffe58f;
  border-radius: 8px;
  padding: 10px 14px;
  margin-top: 8px;
  font-size: 13px;
  color: #d48806;
  text-align: center;
}
.admin-entry {
  text-align: center;
  margin-top: 20px;
  padding: 12px 0;
}
.admin-entry a {
  font-size: 13px;
  color: #999;
  text-decoration: none;
}
.admin-entry a:hover {
  color: #1890ff;
}
</style>
