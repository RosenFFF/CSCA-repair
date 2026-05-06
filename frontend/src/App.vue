<template>
  <router-view />
</template>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}
body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'PingFang SC', 'Hiragino Sans GB', 'Microsoft YaHei', sans-serif;
  background: #f0f2f5;
  -webkit-font-smoothing: antialiased;
  color: #1a1a2e;
}
/* Element Plus overrides for tech feel */
.el-button--primary {
  background: linear-gradient(135deg, #667eea, #764ba2) !important;
  border-color: #667eea !important;
}
.el-button--primary:hover {
  background: linear-gradient(135deg, #5a6fd6, #6a4192) !important;
}
.el-tabs__active-bar {
  background: linear-gradient(90deg, #667eea, #764ba2) !important;
}
</style>
