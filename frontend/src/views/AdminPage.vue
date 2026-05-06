<template>
  <div class="admin-page">
    <!-- Login -->
    <div v-if="!isLoggedIn" class="login-container">
      <div class="login-card">
        <h2>管理后台</h2>
        <el-form @submit.prevent="handleLogin">
          <el-form-item>
            <el-input
              v-model="password"
              type="password"
              placeholder="请输入管理员密码"
              show-password
              size="large"
            />
          </el-form-item>
          <el-button type="primary" size="large" @click="handleLogin" :loading="loggingIn" style="width:100%">
            登录
          </el-button>
        </el-form>
      </div>
    </div>

    <!-- Dashboard -->
    <div v-else class="dashboard">
      <div class="dash-header">
        <h2>管理后台</h2>
        <el-button text @click="logout">退出</el-button>
      </div>

      <el-tabs v-model="activeTab">
        <el-tab-pane label="数据总览" name="stats">
          <StatsCards :stats="stats" />
          <TrendChart :trend="stats.weekly_trend" />
        </el-tab-pane>
        <el-tab-pane label="报名列表" name="list">
          <SignupList />
        </el-tab-pane>
        <el-tab-pane label="排行榜" name="rank">
          <Leaderboard :data="stats.leaderboard" />
        </el-tab-pane>
      </el-tabs>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { adminLogin, getAdminStats } from '../api'
import StatsCards from '../components/StatsCards.vue'
import TrendChart from '../components/TrendChart.vue'
import SignupList from '../components/SignupList.vue'
import Leaderboard from '../components/Leaderboard.vue'

const isLoggedIn = ref(!!localStorage.getItem('admin_token'))
const password = ref('')
const loggingIn = ref(false)
const activeTab = ref('stats')
const stats = ref({
  week_count: 0,
  total_count: 0,
  shift1_count: 0,
  shift2_count: 0,
  weekly_trend: [],
  leaderboard: [],
})

async function handleLogin() {
  if (!password.value) return
  loggingIn.value = true
  try {
    const { data } = await adminLogin(password.value)
    localStorage.setItem('admin_token', data.token)
    isLoggedIn.value = true
    await loadStats()
  } catch {
    ElMessage.error('密码错误')
  } finally {
    loggingIn.value = false
  }
}

function logout() {
  localStorage.removeItem('admin_token')
  isLoggedIn.value = false
}

async function loadStats() {
  try {
    const { data } = await getAdminStats()
    stats.value = data
  } catch {
    // Token expired
    logout()
  }
}

onMounted(() => {
  if (isLoggedIn.value) loadStats()
})
</script>

<style scoped>
.admin-page {
  max-width: 480px;
  margin: 0 auto;
  padding: 20px 16px;
  min-height: 100vh;
}
.login-container {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 80vh;
}
.login-card {
  background: white;
  border-radius: 16px;
  padding: 32px 24px;
  width: 100%;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
}
.login-card h2 {
  text-align: center;
  margin-bottom: 24px;
  font-size: 20px;
}
.dash-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}
.dash-header h2 {
  font-size: 20px;
}
</style>
