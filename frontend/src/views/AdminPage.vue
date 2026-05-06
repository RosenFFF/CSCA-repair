<template>
  <div class="admin-page">
    <!-- Login -->
    <div v-if="!isLoggedIn" class="login-container">
      <div class="login-card">
        <div class="login-header">
          <router-link to="/" class="back-link">&larr; 返回</router-link>
          <div class="login-icon">&#9881;</div>
          <h2>管理员登录</h2>
          <p class="login-sub">请输入管理员密码</p>
        </div>
        <el-form @submit.prevent="handleLogin">
          <el-form-item>
            <el-input
              v-model="password"
              type="password"
              placeholder="密码"
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
        <div class="dash-header-left">
          <router-link to="/" class="back-link">&larr; 返回</router-link>
          <h2>管理后台</h2>
        </div>
        <el-button text @click="logout" class="logout-btn">退出登录</el-button>
      </div>

      <el-tabs v-model="activeTab" class="dash-tabs">
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
  padding: 0 16px 24px;
  min-height: 100vh;
  background: #f0f2f5;
}
.login-container {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 90vh;
}
.login-card {
  background: #fff;
  border-radius: 18px;
  padding: 36px 24px 28px;
  width: 100%;
  box-shadow: 0 4px 24px rgba(0,0,0,0.06);
  border: 1px solid #f0f0f0;
}
.login-header {
  text-align: center;
  margin-bottom: 24px;
  position: relative;
}
.login-icon {
  font-size: 28px;
  color: #667eea;
  margin-bottom: 8px;
}
.login-header h2 {
  font-size: 20px;
  font-weight: 700;
  color: #1a1a2e;
  margin: 0;
}
.login-sub {
  font-size: 13px;
  color: #999;
  margin-top: 4px;
}
.back-link {
  font-size: 13px;
  color: #999;
  text-decoration: none;
  position: absolute;
  left: 0;
  top: 4px;
}
.back-link:hover {
  color: #667eea;
}
.dash-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px 0 12px;
}
.dash-header-left {
  display: flex;
  align-items: center;
  gap: 12px;
}
.dash-header .back-link {
  position: static;
}
.dash-header h2 {
  font-size: 20px;
  font-weight: 700;
  color: #1a1a2e;
  margin: 0;
}
.logout-btn {
  color: #999 !important;
  font-size: 13px;
}
.logout-btn:hover {
  color: #667eea !important;
}
.dash-tabs :deep(.el-tabs__item.is-active) {
  color: #667eea;
}
.dash-tabs :deep(.el-tabs__active-bar) {
  background: linear-gradient(90deg, #667eea, #764ba2);
}
</style>
