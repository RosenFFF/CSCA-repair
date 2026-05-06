<template>
  <div class="signup-page">
    <div class="page-header">
      <div class="header-glow"></div>
      <div class="logo">&#9881;</div>
      <h1>义务维修报名</h1>
      <p class="subtitle">计算机协会 · 每周三下午</p>
    </div>

    <!-- This week -->
    <div class="section" v-if="currentWeekActivities.length">
      <h2 class="section-title">
        <span class="title-dot"></span>
        本周义务维修
      </h2>
      <div class="card-list">
        <ActivityCard
          v-for="(item, idx) in currentWeekActivities"
          :key="item.date + item.shift"
          :activity="item"
          :shiftTitle="idx === 0 ? '第一班次' : '第二班次'"
          @signup="openSignupDialog"
        />
      </div>
    </div>

    <!-- History -->
    <div class="section" v-if="historyActivities.length">
      <el-collapse v-model="expandedHistory">
        <el-collapse-item title="历史记录" name="history">
          <div v-for="(week, idx) in historyGrouped" :key="idx" class="history-week">
            <div class="history-date">{{ formatDate(week.date) }}</div>
            <div class="card-list">
              <ActivityCard
                v-for="(item, i) in week.items"
                :key="item.shift"
                :activity="item"
                :shiftTitle="i === 0 ? '第一班次' : '第二班次'"
                @signup="openSignupDialog"
              />
            </div>
          </div>
        </el-collapse-item>
      </el-collapse>
    </div>

    <!-- Warning -->
    <div class="warning-bar">
      <span class="warning-icon">!</span>
      <span>如果填错或误填，请及时联系部长删除</span>
    </div>

    <!-- Admin Entry -->
    <div class="admin-entry">
      <router-link to="/admin">管理员入口</router-link>
    </div>

    <!-- Signup Dialog -->
    <el-dialog v-model="dialogVisible" title="报名确认" width="90%" :show-close="false" class="signup-dialog">
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
  padding: 0 16px 24px;
  min-height: 100vh;
  background: #f0f2f5;
}
.page-header {
  text-align: center;
  padding: 36px 0 28px;
  position: relative;
  overflow: hidden;
}
.header-glow {
  position: absolute;
  top: -60px;
  left: 50%;
  transform: translateX(-50%);
  width: 260px;
  height: 260px;
  background: radial-gradient(circle, rgba(102,126,234,0.12) 0%, transparent 70%);
  pointer-events: none;
}
.logo {
  font-size: 32px;
  margin-bottom: 6px;
  color: #667eea;
}
h1 {
  font-size: 22px;
  font-weight: 700;
  color: #1a1a2e;
  letter-spacing: 1px;
}
.subtitle {
  font-size: 13px;
  color: #8c8c8c;
  margin-top: 4px;
  letter-spacing: 0.5px;
}
.section-title {
  font-size: 15px;
  font-weight: 600;
  color: #1a1a2e;
  margin-bottom: 12px;
  display: flex;
  align-items: center;
  gap: 8px;
}
.title-dot {
  width: 4px;
  height: 16px;
  background: linear-gradient(180deg, #667eea, #764ba2);
  border-radius: 2px;
  display: inline-block;
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
  font-size: 12px;
  color: #aaa;
  margin-bottom: 8px;
  padding-left: 2px;
}
.warning-bar {
  display: flex;
  align-items: center;
  gap: 8px;
  background: linear-gradient(135deg, #fffbe6, #fff7e6);
  border: 1px solid #ffe58f;
  border-radius: 10px;
  padding: 12px 14px;
  margin-top: 8px;
  font-size: 12px;
  color: #d48806;
}
.warning-icon {
  width: 20px;
  height: 20px;
  background: #faad14;
  color: #fff;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 12px;
  font-weight: 700;
  flex-shrink: 0;
}
.admin-entry {
  text-align: center;
  margin-top: 20px;
  padding: 12px 0;
}
.admin-entry a {
  font-size: 12px;
  color: #bbb;
  text-decoration: none;
  letter-spacing: 0.5px;
}
.admin-entry a:hover {
  color: #667eea;
}
</style>
