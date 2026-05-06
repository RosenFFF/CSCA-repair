import { createRouter, createWebHistory } from 'vue-router'
import SignupPage from '../views/SignupPage.vue'
import AdminPage from '../views/AdminPage.vue'

const routes = [
  { path: '/', component: SignupPage },
  { path: '/admin', component: AdminPage },
]

export default createRouter({
  history: createWebHistory(),
  routes,
})
