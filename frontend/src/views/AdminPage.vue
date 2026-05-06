<template>
  <div class="admin-page">
    <!-- Login -->
    <div v-if="!isLoggedIn" class="login-container">
      <div class="login-card">
        <div class="login-top">
          <router-link to="/" class="back-link">&larr; 返回</router-link>
          <h2>管理后台</h2>
        </div>
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
        <div class="dash-header-left">
          <router-link to="/" class="back-link">&larr; 返回</router-link>
          <h2>管理后台</h2>
        </div>
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
.login-top {
  text-align: center;
  margin-bottom: 24px;
  position: relative;
}
.login-top h2 {
  margin-bottom: 0;
  font-size: 20px;
}
.back-link {
  font-size: 13px;
  color: #999;
  text-decoration: none;
  position: absolute;
  left: 0;
  top: 50%;
  transform: translateY(-50%);
}
.back-link:hover {
  color: #1890ff;
}
.dash-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}
.dash-header-left {
  display: flex;
  align-items: center;
  gap: 12px;
}
.dash-header .back-link {
  position: static;
  transform: none;
}
.dash-header h2 {
  font-size: 20px;
}
</style>
